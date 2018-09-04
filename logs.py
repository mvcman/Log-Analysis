#! /usr/bin/env python3

import psycopg2
DB_NAME = "news"

# 1. What are the most popular three articles of all time?
query1 = """SELECT articles.title,count(*) AS views FROM articles,\
            log WHERE log.path LIKE concat('%',articles.slug) \
            GROUP BY articles.title \
            ORDER BY views DESC LIMIT 3""";

# 2. Who are the most popular article authors of all time?
query2 = """SELECT authors.name,count(*) AS num FROM articles,log,authors\
            WHERE log.path LIKE concat('%',articles.slug)\
            AND articles.author=authors.id \
            GROUP BY authors.name \
            ORDER BY num desc""";

# 3. On which days did more than 1% of requests lead to errors?
query3 = """SELECT TO_CHAR(date :: DATE,'Mon dd,yyyy'),percent_error \
            FROM percentage \
            WHERE percent_error > 1""";

# to store results
query_1_result = dict()

query_2_result = dict()

query_3_result = dict()

# returns query result
def get_query_result(query):
    db = psycopg2.connect(database=DB_NAME)
    c = db.cursor()
    c.execute(query)
    results = c.fetchall()
    db.close()
    return results


def print_articles_query_results(query_result):
    print ("""\n1. The 3 most popular articles of all time are:\n""")
    for result in query_result['results']:
        print ('\t "' + str(result[0]) + '" --- ' + str(result[1]) + ' views')


def print_author_query_results(query_result):
    print ("""\n2. The most popular article authors of
    all time are:\n""")
    for result in query_result['results']:
        print ('\t ' + str(result[0]) + ' --- ' + str(result[1]) + ' views')
        

def print_error_query_results(query_result):
    print ("""\n3. Days with more than 1% of request that
    lead to an error:\n""")
    for result in query_result['results']:
        print ('\t ' + str(result[0]) + ' --- ' + str(result[1]) + ' % errors')


# stores query result
query_1_result['results'] = get_query_result(query1)
query_2_result['results'] = get_query_result(query2)
query_3_result['results'] = get_query_result(query3)

# print formatted output
print_articles_query_results(query_1_result)
print_author_query_results(query_2_result)
print_error_query_results(query_3_result)
