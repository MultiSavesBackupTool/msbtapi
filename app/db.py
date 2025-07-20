import aiomysql
from aiomysql import OperationalError, ProgrammingError
from app import config

pool = None

async def connect_to_db():
    global pool
    try:
        print(f"Attempting to connect to database at {config.db_host}:{config.db_port}")
        pool = await aiomysql.create_pool(
            user=config.db_user,
            password=config.db_password,
            host=config.db_host,
            port=config.db_port,
            db=config.db_name,
            minsize=1,
            maxsize=5,
            autocommit=True
        )
        print("Successfully connected to database")
    except Exception as e:
        print(f"Database connection error: {e}")
        print(f"Connection details: host={config.db_host}, port={config.db_port}, user={config.db_user}, db={config.db_name}")
        pool = None

async def disconnect_from_db():
    global pool
    if pool:
        pool.close()
        await pool.wait_closed()
        print("Disconnected from database")

async def execute_query(query: str):
    global pool
    if pool is None:
        print("Database pool not initialized, attempting to connect...")
        await connect_to_db()
        if pool is None:
            print("Failed to establish database connection")
            return []
    
    try:
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query)
                return await cur.fetchall()
    except OperationalError:
        print("Lost DB connection, trying to reconnect...")
        await connect_to_db()
        return await execute_query(query)
    except ProgrammingError as e:
        print("SQL error:", e)
        return []

async def execute_query_with_params(query: str, params: tuple):
    global pool
    if pool is None:
        print("Database pool not initialized, attempting to connect...")
        await connect_to_db()
        if pool is None:
            print("Failed to establish database connection")
            return []
    
    try:
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query, params)
                if query.strip().lower().startswith('select'):
                    return await cur.fetchall()
    except OperationalError:
        print("Lost DB connection, trying to reconnect...")
        await connect_to_db()
        return await execute_query_with_params(query, params)
    except ProgrammingError as e:
        print("SQL error:", e)
        return []

async def get_blacklist():
    return await execute_query("SELECT * FROM blacklist")

async def get_whitelist():
    return await execute_query("SELECT * FROM whitelist")

async def apply_whitelist(entry: dict):
    query = """
        INSERT INTO whitelist (GameName, SavePath, ModPath, AddPath, SpecialBackupMark)
        VALUES (%s, %s, %s, %s, %s)
    """
    values = (
        entry.get("gameName"),
        entry.get("savePath"),
        entry.get("modPath") or "",
        entry.get("addPath") or "",
        int(entry.get("specialBackupMark", 0))
    )
    await execute_query_with_params(query, values)

async def apply_blacklist(entry: dict):
    query = "INSERT INTO blacklist (GameName) VALUES (%s)"
    values = (entry.get("gameName"),)
    await execute_query_with_params(query, values)