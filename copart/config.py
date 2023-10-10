# Параметры подключения к базе данных
db_config = {
    'host': 'vpromo2.mysql.tools', #ваш хост
    'user': 'vpromo2_usa',# ваше имя пользователя
    'password': '^~Hzd78vG4', # ваш пароль
    'database': 'vpromo2_usa',# имя вашей базы данных
}

# Другие переменные
# """Обновление за сутки"""
url = 'https://www.copart.com/vehicleFinderSearch?displayStr=%5B0%20TO%209999999%5D,%5B2011%20TO%202024%5D&from=%2FvehicleFinder&searchCriteria=%7B%22query%22:%5B%22*%22%5D,%22filter%22:%7B%22NLTS%22:%5B%22expected_sale_assigned_ts_utc:%5BNOW%2FDAY-1DAY%20TO%20NOW%2FDAY%5D%22%5D%7D,%22searchName%22:%22%22,%22watchListOnly%22:false,%22freeFormSearch%22:false%7D'
# """Все объявления"""
# url = 'https://www.copart.com/vehicleFinderSearch?displayStr=%5B0%20TO%209999999%5D,%5B2011%20TO%202024%5D&from=%2FvehicleFinder&searchCriteria=%7B%22query%22:%5B%22*%22%5D,%22filter%22:%7B%7D,%22searchName%22:%22%22,%22watchListOnly%22:false,%22freeFormSearch%22:false%7D'
use_bd = 'vpromo2_usa'
use_table = 'copart'
start_time = "08:30"