# PlayOwnGame-with-DQN
# This project is to train a GAME AI.<br>
For the convenience of training AI, I write a simple game which can accommodate two players.<br>
So I can train the AI by computer against each other. And limited to my time and ability, the game is made very rough.<br> 
But if the AI model trained well, maybe the confrontation process is also wondeful.<br>
<center><img src="https://raw.githubusercontent.com/wyf0912/PlayOwnGame-with-DQN/master/github_img/UI.jpg" width = "300"  alt="游戏界面" align=center /></center><br>
And this is the UI of the game.<br>

## The rule of the game 
>The two boards can be a player or a computer.<br>
 And the boad can move in four directions.<br>
 Getting the ball and making the other player fail to receive will scor.<br>
 And failing to reveive the ball will dock points.<br>
 When a certain difference of score is reached, one of the players win.<br>

## The train modedl of AI
>Because I only have a laptop and a Tencent cloud server without GPU<br>
I didn't use convolutional neural network to deal the image and get the feature, but get the postion of players and the ball by the interface the game reserved when I write it.<br>
Except for no convolutional neural network, the rest of the model is the same as DQN. And I added the number of all connected layers.<br>

## The AI is still training on my laptop and server


