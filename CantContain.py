import psycopg2
import fire
def who_scored():
    table = input("Which table would you like to check out ?") + "_Matches"
    value = ""
    while type(value) != int:
        try:
            value = int(input("You want my to fetch teams that scored ___ goals ?"))
        except ValueError:
            print("Enter a integer only!")


    conn = psycopg2.connect(
        'dbname = gyyopbfd user = gyyopbfd host = 	ziggy.db.elephantsql.com password = ytMQNQ98reIxCDwN6XTwzzWNlLNO5-4q')
    curr = conn.cursor()
    curr.execute("""
        SELECT away from "%s" where "awayscore" = (%s);
        """ %(table,value,))
    Scoring_Teams = [i[0] for i in curr.fetchall()]

    curr.execute("""
        SELECT home from "%s" where "homescore" = (%s);
        """ %(table,value,))
    for i in curr.fetchall():
        Scoring_Teams.append(i[0])
    for team in set(Scoring_Teams):
        times = Scoring_Teams.count(team)
        print(f"{team} has scored {value} goals {times} times this season")


def lose_counter():
    table = input("Which table would you like me to fetch the teams' overall loses?")
    conn = psycopg2.connect(
        'dbname = gyyopbfd user = gyyopbfd host = 	ziggy.db.elephantsql.com password = ytMQNQ98reIxCDwN6XTwzzWNlLNO5-4q')
    curr = conn.cursor()
    curr.execute("""
    SELECT away from "%s" WHERE %s > %s
    """ % (table, "homescore", "awayscore",))
    Loses = [i[0] for i in curr.fetchall()]
    curr.execute("""
        SELECT home from "%s" WHERE %s > %s
        """ % (table, "awayscore", "homescore",))
    for i in curr.fetchall():
        Loses.append(i[0])
    for team in set(Loses):
        print(f"{team} has lost {Loses.count(team)} times so far this season")

def win_counter():
    table = input("Which table would you like me to fetch the teams' overall wins?")
    conn = psycopg2.connect(
        'dbname = gyyopbfd user = gyyopbfd host = 	ziggy.db.elephantsql.com password = ytMQNQ98reIxCDwN6XTwzzWNlLNO5-4q')
    curr = conn.cursor()
    curr.execute("""
    SELECT away from "%s" WHERE %s < %s
    """ % (table, "homescore", "awayscore",))
    Wins = [i[0] for i in curr.fetchall()]
    curr.execute("""
        SELECT home from "%s" WHERE %s < %s
        """ % (table, "awayscore", "homescore",))
    for i in curr.fetchall():
        Wins.append(i[0])
    for team in set(Wins):
        print(f"{team} has won {Wins.count(team)} times so far this season")
        League = table.split('_')
        League = League[:-1]
        if len(League) == 1:
            League = League[0]
        else:
            "_".join(League)

        curr.execute("""
        SELECT "W" from "%s" WHERE squad = '%s'
        """ % (League,team,))
        Wins_From_Table = curr.fetchall()[0][0]
        print(Wins_From_Table)
        assert Wins_From_Table == Wins.count(team)

def data_fetcher():
    table = input("Which league would you like to fetch data from ? \n"
                  "the options are : Pl (Premier League) \ Erevidise \ SerieA \ Bundesliga \ LaLiga \ Ligue1")
    column = input("Which stat would you like to fetch ? \n "
                   "the options are : Pts \ MP \ W \ D \ L \ GF \ GA \ GD")
    value = input("State a value you want to filter the results by \n"
                  "Greater than (>) , Lower than (<) , Equal to (=) , Equal or greater (>=) , Equal or lower (<=) ")
    conn = psycopg2.connect(
        'dbname = gyyopbfd user = gyyopbfd host = 	ziggy.db.elephantsql.com password = ytMQNQ98reIxCDwN6XTwzzWNlLNO5-4q')
    curr = conn.cursor()
    curr.execute(f"""
            SELECT "squad" from "%s" WHERE "%s" %s
            """%(table,column,value,))
    for i in curr.fetchall():
        curr.execute("""
        SELECT "%s" from "%s" WHERE "squad" = '%s'
        """%(column,table,i[0],))
        stat = curr.fetchall()[0][0]
        print(f"{i[0]} matches the value {value} for {column} with {stat}")




def scored_the_most():
    table = input("Which table would you like to get the team that scored the most from ?")
    conn = psycopg2.connect(
        'dbname = gyyopbfd user = gyyopbfd host = 	ziggy.db.elephantsql.com password = ytMQNQ98reIxCDwN6XTwzzWNlLNO5-4q')
    curr = conn.cursor()
    curr.execute("""
    SELECT away from "%s"

    """% (table,))
    Teams = set([str(i[0]) for i in curr.fetchall()])

    Top_Total_Scored = []
    Top_Scorer = ""
    for team in Teams:

        curr.execute("""
            SELECT awayscore from "%s" WHERE away = ('%s');
            """% (table,team,))

        Total_Scored = [i[0] for i in curr.fetchall()]
        curr.execute("""
            SELECT homescore from "%s" WHERE home = ('%s');
            """% (table,team,))
        for i in curr.fetchall():
            Total_Scored.append(i[0])
        if sum(Total_Scored) > sum(Top_Total_Scored):
            Top_Total_Scored = Total_Scored
            Top_Scorer = team

    print(f"The team that scored the most goals this season in the league is {Top_Scorer}! \n"
          f"With a score tally of {sum(Top_Total_Scored)} goals")

if __name__ == "__main__":
    fire.Fire(who_scored)
