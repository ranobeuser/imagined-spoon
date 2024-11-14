class SocialNetwork():
    def __init__(self):
        self.users = {}

    def add_user(self, user):
        username = user.username
        self.users[username] = user
        
    def remove_user(self, username):
        del self.users[username]

    def get_user(self, username):
        return self.users[username]
    
    def get_all_posts(self):
        for i in self.users.values:
            i.get_posts()
        
class Post():
    def __init__(self, content, author):
        self.content = content
        self.author = author
        self.likes = []
        self.comments = []
    
    def like(self,user):
        self.likes.append(user)
    
    def comment(self, content, author):
        new_comment = Comment(content,author)
        self.comments.append(new_comment)

   
class Comment():
    def __init__(self,content,author):
        self.content = content
        self.author = author
        
class User():
    def __init__(self, username):
        self.username = username
        self.friends = []
        self.posts = []
        
    def add_friend(self, user):
        self.friends.append(user)
        
    def remove_friend(self, user):
        self.friends.remove(user)

    def post(content):
        new_post = Post(input("Введите содержание поста"))
        self.posts.append(new_post, self)
    
    def get_posts():
        for i in self.posts:
            print(i.content)
            
            
user1 = User('name1')
user2 = User('name2')

Network1 = SocialNetwork()
Network1.add_user(user1)
Network1.add_user(user2)

user2.add_friend(user1)

post1 = Post('content',user1)

post1.like(user2)

post1.comment('jshdfgjhgfs',user2)

SocialNetwork.get_all_posts()