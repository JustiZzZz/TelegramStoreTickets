import sqlite3
import datetime


def init_db():
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS purchases (
            purchase_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            tariff_type TEXT,
            status TEXT,
            check_photo_id TEXT,
            admin_message_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            question_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            question_text TEXT,
            photo_id TEXT,
            status TEXT,
            user_message_id INTEGER,
            admin_message_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    ''')

    conn.commit()
    conn.close()


def add_user(user_id: int, username: str, first_name: str):
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR IGNORE INTO users (user_id, username, first_name) VALUES (?, ?, ?)",
        (user_id, username, first_name)
    )
    conn.commit()
    conn.close()


def add_question(user_id: int, question_text: str, photo_id: str, user_message_id: int, admin_message_id: int) -> int:
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO questions (user_id, question_text, photo_id, status, user_message_id, admin_message_id) VALUES (?, ?, ?, ?, ?, ?)",
        (user_id, question_text, photo_id, 'pending', user_message_id, admin_message_id)
    )
    conn.commit()
    question_id = cursor.lastrowid
    conn.close()
    return question_id


def get_question_details(question_id: int) -> tuple:
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, question_text, user_message_id FROM questions WHERE question_id = ?",
                   (question_id,))
    result = cursor.fetchone()
    conn.close()
    return result


def mark_question_as_answered(question_id: int):
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE questions SET status = 'answered' WHERE question_id = ?", (question_id,))
    conn.commit()
    conn.close()


def get_pending_questions() -> list:
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT question_id, user_id, question_text, admin_message_id FROM questions WHERE status = 'pending'")
    results = cursor.fetchall()
    conn.close()
    return results


def add_purchase_check(user_id: int, tariff: str, photo_id: str, admin_message_id: int) -> int:
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO purchases (user_id, tariff_type, status, check_photo_id, admin_message_id) VALUES (?, ?, ?, ?, ?)",
        (user_id, tariff, 'pending_approval', photo_id, admin_message_id)
    )
    conn.commit()
    purchase_id = cursor.lastrowid
    conn.close()
    return purchase_id


def update_purchase_status(purchase_id: int, new_status: str):
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE purchases SET status = ? WHERE purchase_id = ?", (new_status, purchase_id))
    conn.commit()
    conn.close()


def get_purchase_details(purchase_id: int) -> tuple:
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, tariff_type FROM purchases WHERE purchase_id = ?", (purchase_id,))
    result = cursor.fetchone()
    conn.close()
    return result


def get_pending_checks() -> list:
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT purchase_id, user_id, tariff_type, admin_message_id FROM purchases WHERE status = 'pending_approval'")
    results = cursor.fetchall()
    conn.close()
    return results


def get_purchase_stats() -> dict:
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT tariff_type, COUNT(*) 
        FROM purchases 
        WHERE status = 'approved' 
        GROUP BY tariff_type
    """)
    results = cursor.fetchall()
    conn.close()

    stats = {"math": 0, "physics": 0, "both": 0}
    for tariff, count in results:
        if tariff in stats:
            stats[tariff] = count

    return stats


def get_advanced_stats() -> dict:
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()

    prices = {"math": 29, "physics": 29, "both": 45}
    stats = {
        'revenue': {'today': 0, 'week': 0, 'month': 0, 'total': 0},
        'sales': {'today': 0, 'week': 0, 'month': 0, 'total': 0},
        'users': {'today': 0, 'week': 0, 'month': 0, 'total': 0},
        'pending': {'checks': 0, 'questions': 0}
    }

    def calculate_metrics(period_filter, time_key):
        query = f"""
            SELECT tariff_type, COUNT(*) 
            FROM purchases 
            WHERE status = 'approved' AND DATE(created_at) >= DATE('now', '{period_filter}')
            GROUP BY tariff_type
        """
        cursor.execute(query)
        results = cursor.fetchall()
        for tariff, count in results:
            stats['revenue'][time_key] += prices.get(tariff, 0) * count
            stats['sales'][time_key] += count

    calculate_metrics('start of day', 'today')
    calculate_metrics('-6 days', 'week')
    calculate_metrics('start of month', 'month')

    cursor.execute("SELECT tariff_type, COUNT(*) FROM purchases WHERE status = 'approved' GROUP BY tariff_type")
    total_results = cursor.fetchall()
    for tariff, count in total_results:
        stats['revenue']['total'] += prices.get(tariff, 0) * count
        stats['sales']['total'] += count

    cursor.execute("SELECT COUNT(*) FROM users WHERE DATE(created_at) >= DATE('now', 'start of day')")
    stats['users']['today'] = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM users WHERE DATE(created_at) >= DATE('now', '-6 days')")
    stats['users']['week'] = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM users WHERE DATE(created_at) >= DATE('now', 'start of month')")
    stats['users']['month'] = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM users")
    stats['users']['total'] = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM purchases WHERE status = 'pending_approval'")
    stats['pending']['checks'] = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM questions WHERE status = 'pending'")
    stats['pending']['questions'] = cursor.fetchone()[0]

    conn.close()
    return stats


def get_user_purchase_history() -> list:
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT u.user_id, u.username, u.first_name, p.tariff_type
        FROM users u
        JOIN purchases p ON u.user_id = p.user_id
        WHERE p.status = 'approved'
        ORDER BY u.user_id
    """)
    results = cursor.fetchall()
    conn.close()
    return results


def wipe_all_data():
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM purchases")
    cursor.execute("DELETE FROM questions")
    cursor.execute("DELETE FROM users")

    cursor.execute("DELETE FROM sqlite_sequence WHERE name IN ('purchases', 'questions')")

    conn.commit()
    conn.close()