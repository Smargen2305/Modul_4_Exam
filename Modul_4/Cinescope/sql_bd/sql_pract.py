#Modul_4\Cinescope\db_requester\sql_alchemy_client_simple_example.py
from examination_4_modul.Modul_4.Cinescope.sql_bd.sql_connection import engine


def sdl_alchemy_SQL():
    query = """
            SELECT id, email, full_name, "password", created_at, updated_at, verified, banned, roles
            FROM public.users
            WHERE id = :user_id;
            """

    # араметры запроса для подстановки в наш SQL запрос
    user_id = "3a172562-e05d-4768-82dd-a098d8e7bbb3"

    # выполняем запрос
    with engine.connect() as connection: #выполняем соединенеи с базой данных и автоматически закрываем его по завершени выполнения
        result = connection.execute(text(query), {"user_id": user_id})
        for row in result:
            print(row)

if __name__ == "__main__":
    sdl_alchemy_SQL()