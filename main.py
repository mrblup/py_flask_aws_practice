
from flask import Flask, render_template, request
import key_config as keys
import boto3 
from boto3.dynamodb.conditions import Key, Attr


app = Flask(__name__)
# MAKE NEW TEMPLATES YO
dynamodb = boto3.resource('dynamodb')
s3 = boto3.client("s3")
@app.route('/')
def index():
    return render_template('signup.html')

    
@app.route('/signup', methods=['post'])
def signup():
    if request.method == 'POST':
        name = request.form['user_name']
        email = request.form['email']
        password = request.form['password']

        # validation here
        table = dynamodb.Table('users')
        response = table.query(
                KeyConditionExpression=Key('email').eq(email)
        )
        items = response['Items']
        if len(items) == 0:
            
            table.put_item(
                    Item={
            'user_name': name,   
            'email': email,
            'password': password
                }
            )
            # need to add in code to say it works in the html
            return render_template("login.html", message = "account has been created")
        # msg = "Registration Complete. Please Login to your account !"
    
        # return render_template('login.html',msg = msg)
        else:
            return render_template('signup.html',message = "account already exists")
    return render_template('signup.html')

@app.route('/login')
def login():    
    return render_template('login.html')


@app.route('/check',methods = ['post'])
def check():
    if request.method=='POST':
        email = request.form['email']
        password = request.form['password']
        
        table = dynamodb.Table('users')
        response = table.query(
                KeyConditionExpression=Key('email').eq(email)
        )
        items = response['Items']
        if len(items) == 0:
            return render_template("login.html", message = "something went wrong, likely no account with that email")
        name = items[0]['user_name']
        print(items[0]['password'])
        if password == items[0]['password']:
            # username = 
         

            # storing username and email into a file as that might work
            with open("username_email.txt", "w") as f:
                f.write(name)
                f.write("\n")
                f.write(email)
                
            # return render_template("home.html",name = name)
            return home()
        else:
            
            return render_template("login.html", message = "either password or email was wrong")
    return render_template("login.html", message = "either password or email was wrong")


def check_empty(artist, title, year):
    table  = dynamodb.Table('music')


    # have to replace this with scan objeccts as dynamodb suck

    if year == "":

        response = table.query(
        KeyConditionExpression=
        Key('artist').eq(artist) & Key('title').eq( title))
        print("2")
        return response["Items"]
    elif artist == "" and year =="":
        response = table.query(
        KeyConditionExpression=
         Key('title').eq( title))
        print("3")
        return response["Items"]
        
    elif title == "" and year =="":
        response = table.query(
        KeyConditionExpression=
        Key('artist').eq(artist)) 
        print("4")
        return response["Items"]
        
        
    elif artist == "" and title =="":
        response = table.query(
        KeyConditionExpression=
         Key('year').eq( year))
        print("5")
        return response["Items"]
        
        
    elif title == "":
        response = table.query(
        KeyConditionExpression=
        Key('artist').eq(artist) & Key('year').eq( year))
        print("6")
        return response["Items"]
        
    
    elif artist == "":
        response = table.query(
        KeyConditionExpression=
        Key('year').eq(year) & Key('title').eq( title))
        print("7")
        return response["Items"]
    else:
        return "---"
        

@app.route("/query", methods = ["get","post"])
def query():
    if request.method == 'POST':
        artist = request.form['Artist']
        title = request.form['Title']
        year = request.form['Year']
        print("aaaaa")
        print(artist)
        # validation here
        table = dynamodb.Table('music')
        # response = table.query(
        #         KeyConditionExpression=Key('email').eq(email)
        # )
     

        if artist== "" and title == "" and year == "":
            print("1")
            return home(query_message = "“No result is retrieved. Please queryagain")
        
           
        
            
        items = check_empty(artist, title, year)
        if len(items) == 0:
            return home()
        elif items == "---":
            return home()
        print(items)

        a = ["a"]
        return home(a)
    return home()

    return
@app.route("/delete_item", methods = ["get","post"])
def delete():
    # if request.method=='POST':
    if request.method=='POST':
        h = request.values
        # this gives me the value of the list, this is gooood
        # print(h[])
        print(h["_token"])
        print("end of delete")
        table = dynamodb.Table('user_sub')

        f = open("username_email.txt", "r")
        data = f.read()
        data = data.split("\n")
        f.close()

        # print(data)
        name = data[0]
        email = data[1]
        # print(email)
        table.delete_item(
            Key = {
                "email":email,
                "title": h["_token"]
            }
        )
        return home()
    print("i")
    return home()



@app.route('/home', methods=["get",'post'])
def home(song_list = None, query_message = None):
    # subs = [1,2,3,4]
    subs = []
    image_url =[]
    test = "2"
    len_subs = 0
    table = dynamodb.Table('user_sub')

    f = open("username_email.txt", "r")
    data = f.read()
    data = data.split("\n")
    f.close()

    print(data)
    name = data[0]
    email = data[1]
    print(email)
    response = table.query(
                KeyConditionExpression=Key('email').eq(email)
        )
    items = response['Items']
    bucket =  "s3895697-music-images"
   
    if len(items) == 0:
        # return render_template("login.html", message = "something went wrong, likely no account with that email")
        subs = ""
        print("bluh")
    else:
        # subs = items[0]["title"]
        for i in items:
            
            b = get_artist(i["title"])
            a = gen_signed_url(bucket,b)
            url = a.split("?")
            subs.append([i["title"],url[0]+".jpg"])
            # image_url.append(url[0]+".jpg")
            # print(url[0])
            len_subs+=1
        print(items)

 
        print("greater than 1")
    if song_list:
        print("bingchiling")
        render_template('home.html',name = name,sub_list = subs,length = len_subs, song_list = song_list)
    # print(a)
    return render_template('home.html',name = name,sub_list = subs,length = len_subs, message = query_message)


def gen_signed_url(bucket_name, object_name):
    url = s3.generate_presigned_url(ClientMethod='get_object',
            Params={'Bucket': bucket_name, 'Key': object_name},
            ExpiresIn=3600)
    # print(url)
    return(url)

def get_artist(song_name):
    table = dynamodb.Table('music')
    response = table.query(
                KeyConditionExpression=Key('title').eq(song_name)
        )
    
    items = response['Items']
    return items[0]["artist"]

if __name__ == '__main__':
      app.run( port=8080, debug=True)




