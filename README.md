# PlayOwnGame-with-DQN
The tools used in the project:<br>
>python 3.5<br>
>tensorflow 1.3.0+<br>
>pygame 1.93<br>
# This project is to train a GAME AI.<br>
For the convenience of training AI, I write a simple game which can accommodate two players.<br>
So I can train the AI by computer against each other. And limited to my time and ability, the game is made very rough. But if the AI model trained well, maybe the confrontation process is also wondeful.<br>
<center><img src="https://raw.githubusercontent.com/wyf0912/PlayOwnGame-with-DQN/master/github_img/UI.jpg" width = "300"  alt="游戏界面" align=center /></center>
And this is the UI of the game.<br>

## The rule of the game 
>The two boards can be a player or a computer.And the boad can move in four directions.<br>
 Getting the ball and making the other player fail to receive will scor.And failing to reveive the ball will dock points.<br>
 When a certain difference of score is reached, one of the players win.<br>

## The train modedl of AI
>Because I only have a laptop and a Tencent cloud server without GPU<br>
I didn't use convolutional neural network to deal the image and get the feature, but get the postion of players and the ball by the interface the game reserved when I write it.<br>
Except for no convolutional neural network, the rest of the model is the same as DQN. And I added the number of all connected layers. 
>### To train two plaers at the same time
>>In order to improe the trainning speed of the network. The two players use the same network at the same time. And for each of the frame, gradient descent will be run for two times. And I don't know if it will cause some problems.

## The AI is still training on my laptop and server
### the problem I met at the moment
I have changed the model several times. But it still didn't work well.<br>
I don't know how to improvement it. 
<center><img src="https://raw.githubusercontent.com/wyf0912/PlayOwnGame-with-DQN/master/github_img/img1.jpg" width = "300"  alt="emmm..." align=center /></center>


