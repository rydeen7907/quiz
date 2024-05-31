"""
4択クイズ

参考元：
https://qiita.com/aksuzuki/items/8d0ccf44bd2893395029

https://daeudaeu.com/tkinter_quiz/#prepare-quiz

リートンで追加・再構築
https://wrtn.jp/
"""

import tkinter
from tkinter import messagebox
import random
import csv

# クイズの情報を格納したファイル
CSV_FILE = "quiz.csv"


class Quiz():
    def __init__(self, master):
        '''コンストラクタ
            master:クイズ画面を配置するウィジェット
        '''

        # 親ウィジェット
        self.master = master

        # クイズデータリスト
        self.quiz_list = []

        # 現在表示中のクイズ
        self.now_quiz = None

        # 現在選択中の選択肢番号
        self.choice_value = tkinter.IntVar()

        # 正解数
        self.correct_answers = 0

        # 出題数
        self.total_questions = 0

        self.getQuiz()
        self.createWidgets()
        self.showQuiz()

    def getQuiz(self):
        '''クイズの情報を取得する'''

        # ファイルを開く
        try:
            f = open(CSV_FILE)
        except FileNotFoundError:
            return None

        # CSVデータとしてファイル読み込み
        csv_data = csv.reader(f)

        # CSVの各行をリスト化
        for quiz in csv_data:
            self.quiz_list.append(quiz)

        f.close()

    def createWidgets(self):
        '''ウィジェットを作成・配置する'''

        # フレームを作成する
        self.frame = tkinter.LabelFrame(
            self.master,
            text="Quiz", # タイトルを設定
            width=450,
            height=200,
        )
        self.frame.pack()

        # ボタンを作成する
        self.button = tkinter.Button(
            self.master,
            text="OK",
            command=self.checkAnswer
        )
        self.button.pack()

    def showQuiz(self):
        '''問題と選択肢を表示'''
        
        if not self.quiz_list:
            print("エラー：クイズリストが空です")
            return

        # まだ表示していないクイズからクイズ情報をランダムに取得
        num_quiz = random.randrange(len(self.quiz_list))
        quiz = self.quiz_list[num_quiz]
        
        # 問題と選択肢合わせて5つ含まれているか
        if len(quiz) < 5:
            print("エラー：クイズデータが不完全です")
            return # データが不完全な場合は処理を中断

        # 問題を表示するラベルを作成
        self.problem = tkinter.Label(
            self.frame,
            text=quiz[0]
        )
        self.problem.grid(
            column=0,
            row=0,
            columnspan=4,
            pady=10
        )

        # 選択肢を表示するラジオボタンを４つ作成
        self.choices = []
        for i in range(4):
            # ラジオボタンウィジェットを作成・配置
            choice = tkinter.Radiobutton(
                self.frame,
                text=quiz[i+1],
                variable=self.choice_value,
                value=i
            )
                
            choice.grid(
                row=1,
                column=i,
                padx=10,
                pady=10,
            )
            # ウィジェットを覚えておく
            self.choices.append(choice)

        # 表示したクイズは再度表示しないようにリストから削除
        self.quiz_list.remove(quiz)

        # 現在表示中のクイズを覚えておく
        self.now_quiz = quiz

        # 出題数を増やす
        self.total_questions += 1

    def deleteQuiz(self):
        '''問題と選択肢を削除'''

        # 問題を表示するラベルを削除
        self.problem.destroy()

        # 選択肢を表示するラジオボタンを削除
        for choice in self.choices:
            choice.destroy()

    def checkAnswer(self):
        '''解答が正解かどうかを表示し、次のクイズを表示する'''

        # 正解かどうかを確認してメッセージを表示
        if self.choice_value.get() == int(self.now_quiz[5]):
            messagebox.showinfo("結果", "正解です(*^_^*)")
            self.correct_answers += 1
        else:
            correct_answer = self.now_quiz[int(self.now_quiz[5]) + 1]
            messagebox.showerror("結果", f"不正解です＞﹏＜\n正解は: {correct_answer}")
        
        # 表示中のクイズを非表示にする
        self.deleteQuiz()

        if self.quiz_list:
            # まだクイズがある場合は次のクイズを表示する
            self.showQuiz()
        else:
            # もうクイズがない場合はアプリを終了する
            self.endAppli()

    def endAppli(self):
        '''アプリを終了する'''

        # クイズがもうないことを表示
        self.problem = tkinter.Label(
            self.frame,
            text=f"クイズは全て出題ずみです。正答率は {self.correct_answers / self.total_questions * 100:.2f}% です。"
        )
        self.problem.grid(
            column=0,
            row=0,
            padx=10,
            pady=10
        )

        # OKボタンのcommandを変更
        self.button.config(
            command=self.master.destroy
        )

app = tkinter.Tk()
quiz = Quiz(app)
app.mainloop()
