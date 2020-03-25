from django import forms
from .models import Topic

class NewTopicForm(forms.ModelForm):
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows':5,'placeholder':'what is on your mind?'}
            # 输入框内的文本
        ),max_length=4000,
        help_text='The max length of the text is 4000.'
        # 提示文本
    )

    class Meta:
        model = Topic
        fields =['subject','message']