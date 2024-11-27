from django import forms
from .models import Exam, Question, ExamSubmission, ExamAnswer

# 考試表單
class ExamForm(forms.ModelForm):
    date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),  # 使用日期時間選擇器
        label='考試日期'
    )

    class Meta:
        model = Exam
        fields = ['title', 'course', 'date', 'duration', 'total_marks']  # 表單欄位
        labels = {
            'title': '考試標題',
            'course': '所屬課程',
            'date': '考試日期',
            'duration': '考試時長',
            'total_marks': '總分數',
        }

# 問題表單
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['exam', 'text', 'option1', 'option2', 'option3', 'option4', 'correct_option', 'marks']  # 表單欄位
        labels = {
            'exam': '所屬考試',
            'text': '問題文本',
            'option1': '選項1',
            'option2': '選項2',
            'option3': '選項3',
            'option4': '選項4',
            'correct_option': '正確選項',
            'marks': '分數',
        }

# 考試提交表單
class ExamSubmissionForm(forms.ModelForm):
    class Meta:
        model = ExamSubmission
        fields = ['exam']  # 表單欄位
        labels = {
            'exam': '所屬考試',
        }

# 考試答案表單
class ExamAnswerForm(forms.ModelForm):
    class Meta:
        model = ExamAnswer
        fields = ['submission', 'question', 'selected_option']  # 表單欄位
        labels = {
            'submission': '所屬提交',
            'question': '所屬問題',
            'selected_option': '選擇的選項',
        }