#
from flask import Flask
from flask_restful import Resource, Api, reqparse, abort

app = Flask(__name__)
api = Api(app)

users = {
    1:{'userid':1,'username':'Michael Jordan','age':'28','team':'Chicago Bulls','position':'point guard'},
    2:{'userid':2,'username':'Stephen Curry','age':'23','team':'Golden States','position':'point guard'},
    3:{'userid':3,'username':'Kevin Durant','age':'22','team':'Phoenix Sun','position':'forward'},
    4:{'userid':4,'username':'Le bon James','age':'28','team':'LA Lakers','position':'forward'},
    5:{'userid':5,'username':'Sharq O\'neal','age':'28','team':'LA Lakers','position':'center'}
}
user_att_list = ['username','age','team','position']

def abort_if_user_doesnt_exist(userid):
    if userid not in users:
        abort(404, message="user {} doesn't exist".format(userid))

parser = reqparse.RequestParser()
# parser.add_argument('user', type=str)
parser.add_argument('userid', type=str)
parser.add_argument('username', type=str)
parser.add_argument('age', type=str)
parser.add_argument('team', type=str)
parser.add_argument('position', type=str)

class userListDemo(Resource):
    def get(self):
        user_list = []
        for key in users.keys():
            user_list.append(users[key])
        return user_list


    def post(self):
        args = parser.parse_args()
        userid = int(max(users.keys())) + 1
        new_user = args
        print(new_user)
        new_user['userid']=userid
        users[userid] = new_user
        return users[userid], 201

class userDemo(Resource):
    def get(self, user_id):
        abort_if_user_doesnt_exist(user_id)
        return users[user_id],200

    def delete(self,user_id):
        abort_if_user_doesnt_exist(user_id)
        del users[user_id]
        return '',204

    def put(self,user_id):
        args = parser.parse_args()
        abort_if_user_doesnt_exist(user_id)
        for attr in user_att_list:
            users[user_id][attr]=args[attr]
        return users[user_id], 201

api.add_resource(userDemo,'/user/<int:user_id>')
api.add_resource(userListDemo,'/users')

if __name__ == '__main__':
    app.run(debug=True)
