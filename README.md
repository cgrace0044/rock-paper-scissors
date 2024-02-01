# Rock Paper Scissors
Rock Paper Scissors is a classic two person game. Players start each round by selecting rock, paper or scissors. Rock crushes scissors, scissors cuts paper, and paper covers rock.
In this project the user plays against the computer over five games to see who wins. 

The game is a mixture of luck and logic.

The live link can be found here - [Rock-Paper-Scissors](https://rock-paper-scissors-caro-43b2048bb224.herokuapp.com/)

![Site Mockup](docs/readme_images/web_display.webp)

## How to Play
- The user plays  games of Rock, Paper, Scissors againsts the computer.
- In each game the user can manually select their play (enter 1 for Paper, 2 for Rock and 3 for Scissors)
  - The computer's choice is randomly selected.
  - In the case of a draw i.e. the user and the computer choose the same hand, the game is run again until there is an outright winner.
  - The winner of each game is printed to the terminal.
  - The overall winner after five games have been played is also printed to the terminal.
- The user's score is saved to the leaderboard.

## Site Owner Goals
- To provide the user with a simple game that is both challenging and rewarding.
- To present the user with an app that functions well and is easy to use. 
- To entice the user to return to the game to improve their score.

## User Stories

- ### As a user I want to:
  - Understand the main purpose of the game via the instructions.
  - Be kept engaged throughout with simple graphics/text which show how the game is progressing.
  - Be challenged by trying to beat the computer.
  - See how many games/rounds I have played.
  - Compare my score to others on the leaderboard.
  - Try and beat my score on the leaderboard

## Logic Flow
ADD LUCID FLOW CHART HERE

![Flow Chart]()

## Features

### Title and Introduction Section
- When the user enters the site they are greeted with the name of the game and are asked to enter their username. 
- The welcome text was created using Pyfiglet which takes ASCII text and renders it into ASCII art fonts. 

![Welcome Screen](docs/readme_images/welcome_page.webp)

- Once the user enters their name the terminal greets them.

![Username Validation](docs/readme_images/username_validation.png)