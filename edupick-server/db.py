"""
database for course datas
"""
file_name = 'course_data.csv'
KEY_LINK = 0
KEY_COURSENAME = 1
KEY_SEMESTER_PERIOD = 2
KEY_REGISTER_PERIOD = 3
KEY_PRICE = 4
KEY_CATEGORY = 5

class DataBase:
    db = []

    def __init__(self):
        with open(file_name, 'r') as file:
            lines = file.read().splitlines()
            for line in lines:
                row = line.split(',')
                row[KEY_PRICE] = int(row[KEY_PRICE])
                row[KEY_REGISTER_PERIOD] = row[KEY_REGISTER_PERIOD].split('~')
                row[KEY_SEMESTER_PERIOD] = row[KEY_SEMESTER_PERIOD].split('~')
                self.db.append(row)

        self.db.sort(key=lambda x: (x[KEY_CATEGORY], x[KEY_COURSENAME], x[KEY_PRICE]))

    def get_categories(self):
        result = []
        category = ""
        for row in self.db:
            if row[KEY_CATEGORY] != category:
                category = row[KEY_CATEGORY]
                result.append(category)
        return result
    
    def get_courselist(self):
        result = []
        name = ""
        for row in self.db:
            if row[KEY_COURSENAME] != name:
                name = row[KEY_COURSENAME]
                result.append(name)
        return result

    def query_course_list(self, query):
        result = []
        for row in self.db:
            if 'name' in query:
                if query['name'] not in row[KEY_COURSENAME]:
                    continue
            if 'category' in query:
                if query['category'] not in row[KEY_CATEGORY]:
                    continue

            result.append(row)
        return result

    def query_course_minprice(self, query):
        result = {}
        for row in self.db:
            if 'name' in query:
                if query['name'] not in row[KEY_COURSENAME]:
                    continue
            if 'category' in query:
                if query['category'] not in row[KEY_CATEGORY]:
                    continue

            name = row[KEY_COURSENAME]
            if name in result:
                result[name]['count'] += 1
                if result[name]['min_price'] > row[KEY_PRICE]:
                    result[name]['min_price'] = row[KEY_PRICE]
            else:
                result[name] = {}
                result[name]['min_price'] = row[KEY_PRICE]
                result[name]['count'] = 1
        
        result_list = []
        for k, v in result.items():
            result_list.append([k, v['min_price'], v['count']])
        return result_list
