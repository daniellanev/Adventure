from bottle import route, run, template, static_file, request
import random
import json
import pymysql

connection = pymysql.connect(host='sql3.freesqldatabase.com',
                             user='sql3157880',
                             password='8KuHU4GkB3',
                             db='sql3157880',
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)

def next_question(q_num = "q1"):
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM sql3157880.question_table AS q LEFT JOIN sql3157880.answer_table AS a ON q.question_id = a.belongs_to WHERE q.question_id ='{}';".format(q_num)
            cursor.execute(sql)
            result = cursor.fetchall()
            return json.dumps(result)
            # return json.dumps({"user": user_id,
            #            "adventure": current_adv_id,
            #            "current": current_story_id,
            #            "text": result,
            #            "image": "troll.png",
            #            "options": next_steps_results
            #            })

    except:
        return json.dumps({'error': 'something is wrong with the DB'})


@route("/", method="GET")
def index():
    return template("adventure.html")

@route("/next_question/<q_num>", method="GET")
def get_next_question(q_num):
    return next_question(q_num)


@route("/start", method="POST")
def start():
    username = request.POST.get("name")
    current_adv_id = request.POST.get("adventure_id")


    user_id = 0 #todo check if exists and if not create it
    current_story_id = 0 #todo change
    next_steps_results = [
        {"id": 1, "option_text": "I fight it"},
        {"id": 2, "option_text": "I give him 10 coins"},
        {"id": 3, "option_text": "I tell it that I just want to go home"},
        {"id": 4, "option_text": "I run away quickly"}
        ]

    #(next_move()

    # todo add the next step based on db
    # return json.dumps({"user": user_id,
    #                    "adventure": current_adv_id,
    #                    "current": current_story_id,
    #                    "text": "You meet a mysterious creature in the woods, what do you do?",
    #                    "image": "troll.png",
    #                    "options": next_steps_results
    #                    })
    #

@route("/story", method="POST")
def story():
    user_id = request.POST.get("user")
    current_adv_id = request.POST.get("adventure")
    next_story_id = request.POST.get("next") #this is what the user chose - use it!
    next_steps_results = [
        {"id": 1, "option_text": "I run!"},
        {"id": 2, "option_text": "I hide!"},
        {"id": 3, "option_text": "I sleep!"},
        {"id": 4, "option_text": "I fight!"}
        ]
    random.shuffle(next_steps_results) #todo change - used only for demonstration purpouses

    #todo add the next step based on db
    return json.dumps({"user": user_id,
                       "adventure": current_adv_id,
                       "text": "New scenario! What would you do?",
                       "image": "choice.jpg",
                       "options": next_steps_results
                       })

@route('/js/<filename:re:.*\.js$>', method='GET')
def javascripts(filename):
    return static_file(filename, root='js')


@route('/css/<filename:re:.*\.css>', method='GET')
def stylesheets(filename):
    return static_file(filename, root='css')


@route('/images/<filename:re:.*\.(jpg|png|gif|ico)>', method='GET')
def images(filename):
    return static_file(filename, root='images')

def main():
    run(host='localhost', port=9000)

if __name__ == '__main__':
    main()

