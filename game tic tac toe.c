#include <stdio.h>

#define SIZE 3

void printBoard(char board[SIZE][SIZE]) {
    printf("Current Board:\n");
    for (int i = 0; i < SIZE; i++) {
        for (int j = 0; j < SIZE; j++) {
            printf(" %c ", board[i][j]);
            if (j < SIZE - 1) printf("|");
        }
        printf("\n");
        if (i < SIZE - 1) printf("---+---+---\n");
    }
}

int checkWin(char board[SIZE][SIZE], char player) {
    
    for (int i = 0; i < SIZE; i++) {
        if (board[i][0] == player && board[i][1] == player && board[i][2] == player) return 1;
        if (board[0][i] == player && board[1][i] == player && board[2][i] == player) return 1;
    }

    
    if (board[0][0] == player && board[1][1] == player && board[2][2] == player) return 1;
    if (board[0][2] == player && board[1][1] == player && board[2][0] == player) return 1;

    return 0;
}

int checkDraw(char board[SIZE][SIZE]) {
    for (int i = 0; i < SIZE; i++) {
        for (int j = 0; j < SIZE; j++) {
            if (board[i][j] == ' ') return 0; 
        }
    }
    return 1; 
}

void playGame() {
    char board[SIZE][SIZE] = {
        {' ', ' ', ' '},
        {' ', ' ', ' '},
        {' ', ' ', ' '}
    };

    char currentPlayer = 'X';
    int row, col;
    int gameWon = 0, gameDraw = 0;

    while (!gameWon && !gameDraw) {
        printBoard(board);
        printf("Player %c, enter row (1-3) and column (1-3): ", currentPlayer);
        scanf("%d %d", &row, &col);

       
        if (row < 1 || row > 3 || col < 1 || col > 3 || board[row-1][col-1] != ' ') {
            printf("Invalid move! Try again.\n");
            continue;
        }

        board[row-1][col-1] = currentPlayer;


        gameWon = checkWin(board, currentPlayer);
        if (gameWon) {
            printBoard(board);
            printf("Player %c wins!\n", currentPlayer);
            break;
        }

       
        gameDraw = checkDraw(board);
        if (gameDraw) {
            printBoard(board);
            printf("It's a draw!\n");
            break;
        }


        currentPlayer = (currentPlayer == 'X') ? 'O' : 'X';
    }
}

int main() {
    printf("Welcome to Tic-Tac-Toe!\n");
    playGame();
    return 0;
}