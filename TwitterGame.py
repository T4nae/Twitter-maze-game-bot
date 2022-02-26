import tweepy
import random
import time
import csv
import os

metrics = {'like': 0, 'retweet': 0, 'reply': 0}

class tweet:
    def __init__(self, TEXT):
        self.TEXT = TEXT
        self.tweet_id = ''
        #access keys    
        self.consumer_token = "c token"
        self.consumer_secret = "c secret"
        self.BEARER= 'bearer'
        self.access_token = "access token"
        self.access_secret = "access secret"
        # Authenticate to Twitter
        self.client = tweepy.Client(bearer_token=self.BEARER, consumer_key=self.consumer_token, consumer_secret=self.consumer_secret, access_token=self.access_token, access_token_secret=self.access_secret,wait_on_rate_limit=True)

    def post(self):
        # post tweet using
        #client.create_tweet(text='text')
        try:
            response = self.client.create_tweet(text=self.TEXT)
        except tweepy.Forbidden:
            if len(self.TEXT) >= 280:
                self.check()
            else:                
                self.TEXT = self.TEXT + '.'
            self.post()
            return
        tweet = response.data


        self.tweet_id = tweet['id']
        self.save()
        #print(self.tweet_id)

    def delete(self, id):
        self.client.delete_tweet(id)
        print('deleted')

    def get_metrics(self):
        global metrics
        response = self.client.get_tweet(id = self.tweet_id,tweet_fields='public_metrics')
        print(response.data)
        tweets = response.data
        metrics['like'] = tweets["public_metrics"]["like_count"]
        metrics['retweet'] = tweets["public_metrics"]["retweet_count"]
        metrics['reply'] = tweets["public_metrics"]["reply_count"]
        if (metrics['like'] > metrics['reply'] ) and (metrics['like'] > metrics['retweet'] ):
            largest = 'l'
        elif (metrics['reply']  > metrics['like']) and (metrics['reply']  > metrics['retweet'] ):
            largest = 'r'
        else:
            largest = 'f'
        #print(metrics)
        return largest
        
    def save(self):
        if os.path.exists('tweets.csv') == False:
            with open('tweets.csv' , 'w') as file:
                pass
    
        with open('tweets.csv' , 'a') as file:
                write = csv.writer(file)
                fields = [self.TEXT, self.tweet_id]
                write.writerow(fields)

    def check(self):
        rows = []
        
        with open('tweets.csv' , 'r') as file:
            read = csv.reader(file)
            for row in read:
                if row[0] == self.TEXT:
                    self.delete(row[1])
                else:
                    rows.append(row)                  
        with open('tweets.csv' , 'w') as file:
            write = csv.writer(file)
            write.writerows(rows)

    def deleteall(self):
        while True:
            try:
                response = self.client.get_users_tweets(id = self.user_id,max_results= 100)
                tweets = response.data
                for tweet in tweets:
                    self.delete(tweet['id'])
            except:
                pass
                                                                    
class maze:
    def __init__(self, height, width):
        self.maze = list()
        self.currentcell = list()
        self.height = height
        self.width = width
        self.MazeText = str()
        self.start = list()
        self.finish = list()
        self.currentcell = list()
    ## Functions
    
    def printMaze(self):
    	#print(self.maze)
    	self.MazeText = ''
    	for i in range(0, self.height):
    		for j in range(0, self.width):
    			if (self.maze[i][j] == 'u'):
    				self.MazeText = self.MazeText + '🔴'
    			elif (self.maze[i][j] == 'c'):
    				self.MazeText = self.MazeText + '⚪'
    			else:
    				self.MazeText = self.MazeText + '⚫'
    			
    		self.MazeText = self.MazeText + '\n'
    	#print(self.MazeText)
    	return self.MazeText

    def get_starting_finishing_points(self):
        _start = [i for i in range(len(self.maze[0])) if self.maze[0][i] == 'c']
        _end = [i for i in range(len(self.maze[0])) if self.maze[len(self.maze)-1][i] == 'c']
        self.start , self.finish = [0, _start[0]], [len(self.maze) - 1, _end[0]]    
        self.currentcell = self.start      
        self.maze[self.currentcell[0]][self.currentcell[1]] = 'u'
        #print(self.maze[self.currentcell[0]][self.currentcell[1]])
        
    # Find number of surrounding cells
    def surroundingCells(self, rand_wall):
    	s_cells = 0
    	if (self.maze[rand_wall[0]-1][rand_wall[1]] == 'c'):
    		s_cells += 1
    	if (self.maze[rand_wall[0]+1][rand_wall[1]] == 'c'):
    		s_cells += 1
    	if (self.maze[rand_wall[0]][rand_wall[1]-1] == 'c'):
    		s_cells +=1
    	if (self.maze[rand_wall[0]][rand_wall[1]+1] == 'c'):
    		s_cells += 1
    
    	return s_cells
    
    


    def generate(self):
        ## Main maze code
        # Init variables
        wall = 'w'  # game over if collide
        cell = 'c'    # empty spaces
        unvisited = 'u'    # maze generator and cell travelled
      
        # Denote all cells as unvisited
        for i in range(0, self.height):
        	line = []
        	for j in range(0, self.width):
        		line.append(unvisited)
        	self.maze.append(line)
        
        # Randomize starting point and set it a cell
        starting_height = int(random.random()*self.height)
        starting_width = int(random.random()*self.width)
        if (starting_height == 0):
        	starting_height += 1
        if (starting_height == self.height-1):
        	starting_height -= 1
        if (starting_width == 0):
        	starting_width += 1
        if (starting_width == self.width-1):
        	starting_width -= 1
        
        # Mark it as cell and add surrounding walls to the list
        self.maze[starting_height][starting_width] = cell
        walls = []
        walls.append([starting_height - 1, starting_width])
        walls.append([starting_height, starting_width - 1])
        walls.append([starting_height, starting_width + 1])
        walls.append([starting_height + 1, starting_width])
        
        # Denote walls in maze
        self.maze[starting_height-1][starting_width] = 'w'
        self.maze[starting_height][starting_width - 1] = 'w'
        self.maze[starting_height][starting_width + 1] = 'w'
        self.maze[starting_height + 1][starting_width] = 'w'
        
        while (walls):
        	# Pick a random wall
        	rand_wall = walls[int(random.random()*len(walls))-1]
        
        	# Check if it is a left wall
        	if (rand_wall[1] != 0):
        		if (self.maze[rand_wall[0]][rand_wall[1]-1] == 'u' and self.maze[rand_wall[0]][rand_wall[1]+1] == 'c'):
        			# Find the number of surrounding cells
        			s_cells = self.surroundingCells(rand_wall)
        
        			if (s_cells < 2):
        				# Denote the new path
        				self.maze[rand_wall[0]][rand_wall[1]] = 'c'
        
        				# Mark the new walls
        				# Upper cell
        				if (rand_wall[0] != 0):
        					if (self.maze[rand_wall[0]-1][rand_wall[1]] != 'c'):
        						self.maze[rand_wall[0]-1][rand_wall[1]] = 'w'
        					if ([rand_wall[0]-1, rand_wall[1]] not in walls):
        						walls.append([rand_wall[0]-1, rand_wall[1]])
        
        
        				# Bottom cell
        				if (rand_wall[0] != self.height-1):
        					if (self.maze[rand_wall[0]+1][rand_wall[1]] != 'c'):
        						self.maze[rand_wall[0]+1][rand_wall[1]] = 'w'
        					if ([rand_wall[0]+1, rand_wall[1]] not in walls):
        						walls.append([rand_wall[0]+1, rand_wall[1]])
        
        				# Leftmost cell
        				if (rand_wall[1] != 0):	
        					if (self.maze[rand_wall[0]][rand_wall[1]-1] != 'c'):
        						self.maze[rand_wall[0]][rand_wall[1]-1] = 'w'
        					if ([rand_wall[0], rand_wall[1]-1] not in walls):
        						walls.append([rand_wall[0], rand_wall[1]-1])
        			
        
        			# Delete wall
        			for wall in walls:
        				if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
        					walls.remove(wall)
        
        			continue
        
        	# Check if it is an upper wall
        	if (rand_wall[0] != 0):
        		if (self.maze[rand_wall[0]-1][rand_wall[1]] == 'u' and self.maze[rand_wall[0]+1][rand_wall[1]] == 'c'):
        
        			s_cells = self.surroundingCells(rand_wall)
        			if (s_cells < 2):
        				# Denote the new path
        				self.maze[rand_wall[0]][rand_wall[1]] = 'c'
        
        				# Mark the new walls
        				# Upper cell
        				if (rand_wall[0] != 0):
        					if (self.maze[rand_wall[0]-1][rand_wall[1]] != 'c'):
        						self.maze[rand_wall[0]-1][rand_wall[1]] = 'w'
        					if ([rand_wall[0]-1, rand_wall[1]] not in walls):
        						walls.append([rand_wall[0]-1, rand_wall[1]])
        
        				# Leftmost cell
        				if (rand_wall[1] != 0):
        					if (self.maze[rand_wall[0]][rand_wall[1]-1] != 'c'):
        						self.maze[rand_wall[0]][rand_wall[1]-1] = 'w'
        					if ([rand_wall[0], rand_wall[1]-1] not in walls):
        						walls.append([rand_wall[0], rand_wall[1]-1])
        
        				# Rightmost cell
        				if (rand_wall[1] != self.width-1):
        					if (self.maze[rand_wall[0]][rand_wall[1]+1] != 'c'):
        						self.maze[rand_wall[0]][rand_wall[1]+1] = 'w'
        					if ([rand_wall[0], rand_wall[1]+1] not in walls):
        						walls.append([rand_wall[0], rand_wall[1]+1])
        
        			# Delete wall
        			for wall in walls:
        				if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
        					walls.remove(wall)
        
        			continue
        
        	# Check the bottom wall
        	if (rand_wall[0] != self.height-1):
        		if (self.maze[rand_wall[0]+1][rand_wall[1]] == 'u' and self.maze[rand_wall[0]-1][rand_wall[1]] == 'c'):
        
        			s_cells = self.surroundingCells(rand_wall)
        			if (s_cells < 2):
        				# Denote the new path
        				self.maze[rand_wall[0]][rand_wall[1]] = 'c'
        
        				# Mark the new walls
        				if (rand_wall[0] != self.height-1):
        					if (self.maze[rand_wall[0]+1][rand_wall[1]] != 'c'):
        						self.maze[rand_wall[0]+1][rand_wall[1]] = 'w'
        					if ([rand_wall[0]+1, rand_wall[1]] not in walls):
        						walls.append([rand_wall[0]+1, rand_wall[1]])
        				if (rand_wall[1] != 0):
        					if (self.maze[rand_wall[0]][rand_wall[1]-1] != 'c'):
        						self.maze[rand_wall[0]][rand_wall[1]-1] = 'w'
        					if ([rand_wall[0], rand_wall[1]-1] not in walls):
        						walls.append([rand_wall[0], rand_wall[1]-1])
        				if (rand_wall[1] != self.width-1):
        					if (self.maze[rand_wall[0]][rand_wall[1]+1] != 'c'):
        						self.maze[rand_wall[0]][rand_wall[1]+1] = 'w'
        					if ([rand_wall[0], rand_wall[1]+1] not in walls):
        						walls.append([rand_wall[0], rand_wall[1]+1])
        
        			# Delete wall
        			for wall in walls:
        				if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
        					walls.remove(wall)
        
        
        			continue
        
        	# Check the right wall
        	if (rand_wall[1] != self.width-1):
        		if (self.maze[rand_wall[0]][rand_wall[1]+1] == 'u' and self.maze[rand_wall[0]][rand_wall[1]-1] == 'c'):
        
        			s_cells = self.surroundingCells(rand_wall)
        			if (s_cells < 2):
        				# Denote the new path
        				self.maze[rand_wall[0]][rand_wall[1]] = 'c'
        
        				# Mark the new walls
        				if (rand_wall[1] != self.width-1):
        					if (self.maze[rand_wall[0]][rand_wall[1]+1] != 'c'):
        						self.maze[rand_wall[0]][rand_wall[1]+1] = 'w'
        					if ([rand_wall[0], rand_wall[1]+1] not in walls):
        						walls.append([rand_wall[0], rand_wall[1]+1])
        				if (rand_wall[0] != self.height-1):
        					if (self.maze[rand_wall[0]+1][rand_wall[1]] != 'c'):
        						self.maze[rand_wall[0]+1][rand_wall[1]] = 'w'
        					if ([rand_wall[0]+1, rand_wall[1]] not in walls):
        						walls.append([rand_wall[0]+1, rand_wall[1]])
        				if (rand_wall[0] != 0):	
        					if (self.maze[rand_wall[0]-1][rand_wall[1]] != 'c'):
        						self.maze[rand_wall[0]-1][rand_wall[1]] = 'w'
        					if ([rand_wall[0]-1, rand_wall[1]] not in walls):
        						walls.append([rand_wall[0]-1, rand_wall[1]])
        
        			# Delete wall
        			for wall in walls:
        				if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
        					walls.remove(wall)
        
        			continue
        
        	# Delete the wall from the list anyway
        	for wall in walls:
        		if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
        			walls.remove(wall)
        	
        
        
        # Mark the remaining unvisited cells as walls
        for i in range(0, self.height):
        	for j in range(0, self.width):
        		if (self.maze[i][j] == 'u'):
        			self.maze[i][j] = 'w'
        
        # Set entrance and exit
        for i in range(0, self.width):
        	if (self.maze[1][i] == 'c'):
        		self.maze[0][i] = 'c'
        		break
        
        for i in range(self.width-1, 0, -1):
        	if (self.maze[self.height-2][i] == 'c'):
        		self.maze[self.height-1][i] = 'c'
        		break
        self.get_starting_finishing_points()
    
    def update(self, input):
        # inputs
        if input == 'l': #left like
            self.currentcell[1] = self.currentcell[1] - 1
        if input == 'r': #rigth reply
            self.currentcell[1] = self.currentcell[1] + 1
        if input == 'f': #forward retweet
            self.currentcell[0] = self.currentcell[0] + 1
               
        # conditions
        if self.maze[self.currentcell[0]][self.currentcell[1]] == 'w': # wall
            return 'lost'
        elif self.maze[self.currentcell[0]][self.currentcell[1]] == 'c': #empty cell
            self.maze[self.currentcell[0]][self.currentcell[1]] = 'u'       
        # win condition
        if self.currentcell == self.finish: #win
            return 'won'

def main():
    height = 4
    width = 4
    score = 0

    while True:
        # get highscore
        if os.path.exists('highscore.txt') == False:
                 with open('highscore.txt' , 'w') as file:
                     file.write('0')
        with open('highscore.txt' , 'r') as file:
            highscore = int(file.read())    
        # difficulty and score incriment
        if height <= 8 and width <= 8:
            height = height + 1
            width = width + 1
        score = score + 1
        
        # gameplay
        game = maze(height, width)
        game.generate()
        
        while True:
            board =  game.printMaze()
            tweets = tweet('HighScore: ' + str(highscore) + ', CurrentScore: ' + str(score) + '\n' + board + '\nreply ⬅️  retweet ⬇️  like ➡️\n')
            tweets.post()
            time.sleep(360)  # 360 sec or 6mins
            inp = tweets.get_metrics()
            result = game.update(inp)
            
            if result == 'won':
                won = tweet('HighScore: ' + str(highscore) + ', CurrentScore: ' + str(score) + '\n' + board + '\nWON\n')
                won.post()                
                del game
                break
            elif result == 'lost':
                lost = tweet('HighScore: ' + str(highscore) + ', CurrentScore: ' + str(score) + '\n' + board + '\nLost\n')
                lost.post() 
                if score > highscore:
                    with open('highscore.txt' , 'w') as file:
                        highscore = file.write(str(score))
                        
                # reset maze size and score                        
                height , width = 4, 4
                score = 0
                break



if __name__ == '__main__':
    main()  
