#coding=utf-8
from django import forms  
from django.contrib.auth.models import User 
from captcha.fields import CaptchaField
      
# 登录表单
class LoginForm(forms.Form):  
    username = forms.CharField(  
            required=True,  
            label=u"用户名",  
            error_messages={'required': '请输入用户名'},  
            widget=forms.TextInput(  
                attrs={  
                    'placeholder':u"用户名",  
                }  
            ),  
    )      
    password = forms.CharField(  
            required=True,  
            label=u"密码",  
            error_messages={'required': u'请输入密码'},  
            widget=forms.PasswordInput(  
                attrs={  
                    'placeholder':u"密码",  
                }  
            ),  
    )     
    def clean(self):  
        if not self.is_valid():  
            raise forms.ValidationError(u"用户名和密码为必填项")  
        else:  
            cleaned_data = super(LoginForm, self).clean() 

# 注册表单
class RegistForm(forms.Form):
    username = forms.CharField(
        required=True,
        label=u'用户名',
        error_messages={'required': '请输入用户名'},  
            widget=forms.TextInput(  
                attrs={  
                    'placeholder':u"用户名",  
                }  
            ),
    )  
    password = forms.CharField(  
            required=True,  
            label=u"密码",  
            error_messages={'required': u'请输入密码'},  
            widget=forms.PasswordInput(  
                attrs={  
                    'placeholder':u"密码",  
                }  
            ),  
    ) 
    password_again = forms.CharField(  
            required=True,  
            label=u"再次输入密码",  
            error_messages={'required': u'请输入密码'},  
            widget=forms.PasswordInput(  
                attrs={  
                    'placeholder':u"密码",  
                }  
            ),  
    )

    email = forms.CharField(  
            required=True,  
            label=u"邮箱地址",  
            error_messages={'required': u'请输入邮箱'},  
            widget=forms.TextInput(  
                attrs={  
                    'placeholder':u"邮箱",  
                }  
            ),  
    )

    #captcha = CaptchaField()
    
    def clean(self):  
        if not self.is_valid():  
            raise forms.ValidationError(u"请重新确认填写是否有误")  
        else:  
            cleaned_data = super(RegistForm, self).clean()
