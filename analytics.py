#!/usr/bin/env pytjon3

import psycopg2


def top_three_articles():
    """ Return the top three articles from the database """

    # connect to the database
    conn = psycopg2.connect("dbname=news user=postgres")

    curr = conn.cursor()

    # query to run
    # reference
    # https://stackoverflow.com/questions/15378216/postgresql-contains-in-where-clause
    query = '''SELECT articles.title, count(*) as num FROM log, articles
               WHERE log.path = '/article/' || articles.slug
                   AND log.status = '200 OK'
               GROUP BY articles.title
               ORDER BY num DESC LIMIT 3;'''

    curr.execute(query)

    results = curr.fetchall()

    # go through each result and print to screen
    for result in results:
        title = result[0]
        views = str(result[1])

        print(title + " (" + views + " views)")

    # close connection to database
    curr.close()
    conn.close()

    return


def top_authors():
    """ Get the authors with the most views on their articles """

    # connect to the database
    conn = psycopg2.connect("dbname=news user=postgres")

    curr = conn.cursor()

    # query to run
    # reference:
    # https://stackoverflow.com/questions/15378216/postgresql-contains-in-where-clause
    query = '''SELECT authors.name, count(*) as num FROM log, articles, authors
             WHERE log.path = '/article/' || articles.slug
                 AND authors.id = articles.author
                 AND log.status = '200 OK'
             GROUP BY authors.name
             ORDER BY num DESC LIMIT 3;'''

    curr.execute(query)

    results = curr.fetchall()

    # go through all the authors and print to screen
    for result in results:
        title = result[0]
        views = str(result[1])

        print(title + " (" + views + " views)")

    # close connection to database
    curr.close()
    conn.close()

    return


def error_days():
    """ Get the days with more than 1% errors """

    # connect to the database
    conn = psycopg2.connect("dbname=news user=postgres")

    curr = conn.cursor()

    # query to run
    # reference
    # https://stackoverflow.com/questions/15378216/postgresql-contains-in-where-clause
    query_avg = '''
              WITH error_counts AS (
                SELECT date_trunc('day', time) as day,
                  CAST(COUNT(*) AS FLOAT) as num
                FROM log
                WHERE STATUS != '200 OK'
                GROUP BY day),
              total_counts AS (
                SELECT date_trunc('day', time) AS day,
                   CAST(COUNT(*) AS FLOAT) AS total_num
                FROM log
                GROUP BY day)
              SELECT
                to_char(total_counts.day, 'Month DD YYYY') AS day,
                (error_counts.num / total_counts.total_num * 100) as percent
              FROM total_counts, error_counts
              WHERE error_counts.day = total_counts.day
              ORDER BY percent DESC
              LIMIT 1;
              '''

    curr.execute(query_avg)

    results = curr.fetchall()

    # go through each day and print to screen
    for result in results:
        date = result[0].replace("     ", "")
        percent = result[1]
        print(date + " (" + str(percent[:3]) + "% errors)")

    # close connection to database
    curr.close()
    conn.close()

    return


def main():
    """ Run all the functions to grab analytics from the database """

    print("Top Three Articles")
    print("------------------")
    top_three_articles()

    print("\nTop Authors")
    print("-----------")
    top_authors()

    print("\nDays With >1% Errors")
    print("--------------------")
    error_days()

    return

# run the program
if __name__ == "__main__":
    main()
