import json
import psycopg2

def cleanStr4SQL(s):
    return s.replace("'","`").replace("\n"," ")


def int2BoolStr (value):
    if value == 0:
        return 'False'
    else:
        return 'True'

def parseDicts(d):
    out = []
    for (k, v) in d.items():
        if isinstance(v,dict):
            out = out + parseDicts(v)
        else :
            out.append((k,v))

    return out

def insert2BusinessTable():
    #reading the JSON file
    with open('yelp_business.JSON','r') as f:
        line = f.readline()
        count_line = 0
        #connect to yelpdb database on postgres server using psycopg2
        try:
            #TO DO: update the database name, username, and password
            conn = psycopg2.connect("dbname='Check_project' user='postgres' host='localhost' password='fiona123'")
        except:
            print('Unable to connect to the database!')
        cur = conn.cursor()
        while line:
            data = json.loads(line)
            try:
                #categories, attributes?
                cur.execute("INSERT INTO yelp_business (business_id, name, address,state, city, postal_code, latitude, longitude, stars, numcheckins, numtips, is_open)"+ " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)",
                            (data['business_id'],cleanStr4SQL(data["name"]),
                             cleanStr4SQL(data["address"]), data["state"], data["city"], data["postal_code"],
                             data["latitude"], data["longitude"], data["stars"], 0 , 0 ,
                             data["is_open"] ) )
            except Exception as e:
                print("Insert to businessTABLE failed!",e)
            conn.commit()
            line = f.readline()
            count_line +=1
        cur.close()
        conn.close()
        print(count_line)
    f.close()

def insert2Tips_table():
    #reading the JSON file
    with open('yelp_tip.JSON','r') as f:
        line = f.readline()
        count_line = 0

        #connect to yelpdb database on postgres server using psycopg2
        try:
            conn = psycopg2.connect("dbname='Check_project' user='postgres' host='localhost' password ='fiona123'")
        except:
            print('Unable to connect to the database!')
        cur = conn.cursor()

        while line:
            data = json.loads(line)
            try:
                cur.execute("INSERT INTO yelp_tips (user_id,business_id,date,likes,text)"
                            + " VALUES (%s, %s, %s, %s, %s)",
                            ((data["user_id"],(data["business_id"]), (data["date"]), (data["likes"]), cleanStr4SQL(data["text"]))) )
            except Exception as e:
                print("Insert to yelp_tips failed!" ,e)
            conn.commit()

            line = f.readline()
            count_line += 1

        cur.close()
        conn.close()

    print(count_line)
    #outfile.close()  #uncomment this line if you are writing the INSERT statements to an output file.
    f.close()

def insert2Users_table():
    #reading the JSON file
    with open('yelp_user.JSON','r') as f:
        line = f.readline()
        count_line = 0

        try:
            conn = psycopg2.connect("dbname='Check_project' user='postgres' host='localhost' password ='fiona123'")
        except:
            print('Unable to connect to the database!')
        cur = conn.cursor()

        while line:
            data = json.loads(line)

            try:
                cur.execute("INSERT INTO yelp_user (user_id,cool,fans,funny,name,tipcount,useful,yelping_since,user_latitude,user_longitude,totallikes,average_stars)"
                            + " VALUES (%s, %s, %s, %s, %s,%s,%s,%s,%s,%s, %s, %s)",
                            ((data["user_id"],(data["cool"]), (data["fans"]), (data["funny"]), (data["name"]), (data["tipcount"]), (data["useful"]) ,(data["yelping_since"]) , 0,0,0, (data["average_stars"]))) )
            except Exception as e:
                print("Insert to yelp_user failed!" ,e)
            conn.commit()

            line = f.readline()
            count_line += 1

        cur.close()
        conn.close()

    print(count_line)
    #outfile.close()  #uncomment this line if you are writing the INSERT statements to an output file.
    f.close()

def insert2Attributes():
    with open('yelp_business.JSON','r') as f:
        line = f.readline()
        count_line = 0
        #connect to yelpdb database on postgres server using psycopg2
        try:
            #TO DO: update the database name, username, and password
            conn = psycopg2.connect("dbname='Check_project' user='postgres' host='localhost' password='fiona123'")
        except:
            print('Unable to connect to the database!')
        cur = conn.cursor()
        while line:
            data = json.loads(line)
            attributes = data["attributes"]
            attr =parseDicts(attributes)
            bid = data['business_id']
            count = 0
            for aname, value in attr:
                attributeName = aname
                attrValue = value
                count+=1
                print(count_line)
                try:
                    #categories, attributes?
                    cur.execute("INSERT INTO attributes(business_id, attr_name,value)"+ " VALUES (%s, %s, %s)",
                                (bid,attributeName, attrValue))
                except Exception as e:
                    print("Insert to attributes TABLE failed!",e)
                conn.commit()
            line = f.readline()
            count_line +=1
        cur.close()
        conn.close()
        print(count_line)
    f.close()

def insert2Categories():
    with open('yelp_business.JSON','r') as f:
        line = f.readline()
        count_line = 0
        #connect to yelpdb database on postgres server using psycopg2
        try:
            #TO DO: update the database name, username, and password
            conn = psycopg2.connect("dbname='Check_project' user='postgres' host='localhost' password='fiona123'")
        except:
            print('Unable to connect to the database!')
        cur = conn.cursor()
        while line:
            data = json.loads(line)
            categories = data["categories"].split(', ')
            bid = data['business_id']
            for cat in categories:
                try:
                    cur.execute("INSERT INTO categories(business_id, category_name)"+ " VALUES (%s, %s)",
                                (bid,cat) )
                except Exception as e:
                    print("Insert to categoriesTABLE failed!",e)
                conn.commit()
            line = f.readline()
            count_line +=1
        cur.close()
        conn.close()
        print(count_line)

    f.close()

def insert2Friends():
    with open('yelp_user.JSON','r') as f:
        #TO DO: update path for the inputfile
        line = f.readline()
        count_line = 0
        try:
            #TO DO: update the database name, username, and password
            conn = psycopg2.connect("dbname='Check_project' user='postgres' host='localhost' password='fiona123'")
        except:
            print('Unable to connect to the database!')
        cur = conn.cursor()
        while line:
            data = json.loads(line)
            friends = data["friends"]
            user_1 =data['user_id']
            for fr in friends:
                try:
                    cur.execute("INSERT INTO friends(user_id_1, user_id_2)"+ " VALUES (%s, %s)",
                                (user_1,fr) )
                except Exception as e:
                    print("Insert to friendsTABLE failed!",e)
                conn.commit()
            line = f.readline()
            count_line +=1
        cur.close()
        conn.close()
        print(count_line)

    f.close()

def insert2Hours():
    with open('yelp_business.JSON','r') as f:
        line = f.readline()
        count_line = 0
        try:
            conn = psycopg2.connect("dbname='Check_project' user='postgres' host='localhost' password='fiona123'")
        except:
            print('Unable to connect to the database!')
        cur = conn.cursor()
        while line:
            data = json.loads(line)
            hours = data["hours"]
            for (dow, times) in hours.items():
                day = dow
                openTime = times.split('-')[0]
                closeTime = times.split('-')[1]

            try:
                cur.execute("INSERT INTO hours(business_id,dayofweek,open,close)"+ " VALUES (%s, %s,%s,%s)",
                            (data['business_id'],day,openTime,closeTime))
            except Exception as e:
                print("Insert to hours TABLE failed!",e)
            conn.commit()
            line = f.readline()
            count_line +=1
        cur.close()
        conn.close()
        print(count_line)
    f.close()


def insert2CheckInTable():
    #reading the JSON file
    with open('yelp_checkin.JSON','r') as f:
        line = f.readline()
        count_line = 0
        try:
            conn = psycopg2.connect("dbname='Check_project' user='postgres' host='localhost' password='fiona123'")
        except:
            print('Unable to connect to the database!')
        cur = conn.cursor()
        while line:
            data = json.loads(line)
            checkindates =data['date'].split(',')
            bid = data['business_id']
            for timestamp in checkindates:
                try:
                    cur.execute("INSERT INTO checkins (business_id, checkin_time)"+ " VALUES (%s, %s)",
                                (bid,timestamp) )
                except Exception as e:
                    print("Insert to checkinTABLE failed!",e)
                conn.commit()
            line = f.readline()
            count_line +=1
        cur.close()
        conn.close()
        print(count_line)
    f.close()



if __name__ == "__main__":
    #insert2BusinessTable()
    #insert2CheckInTable()
    #insert2Tips_table()
    #insert2Users_table()
    #insert2Attributes()
    #insert2Categories()
    #insert2Friends()
    insert2Hours()

    #I have already inserted everything so I'm not going to "run" these statements
    #To avoid the error showing, I use PASS, but it is not going to show any results
    # pass

