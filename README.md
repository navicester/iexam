## 怎样创建关联formset
How to create link formset
### 定义关联form - LinkFormAdminForm
Define link form
``` python
class WordExpForm(LinkFormAdminForm):
    class Meta:
        verbose_name = 'Word Exp'
        class_name = "WordExp"
        
    id = forms.CharField(max_length=11, label = "id", widget = forms.TextInput(attrs={'readonly':'readonly','disable':True})) 
    phonetic = forms.CharField(max_length=11, label = "phonetic", required=False, widget = 
                             forms.TextInput(attrs={'readonly':'readonly','disable':True}))    
    explain = forms.CharField(max_length=50, label = "explain", required=False, widget = 
                             forms.TextInput(attrs={'readonly':'readonly','disable':True}))    
    sentence = forms.CharField(max_length=11, label = "sentence", required=False, widget = 
                             forms.TextInput(attrs={'readonly':'readonly','disable':True}))  
    book = forms.CharField(max_length=11, label = "book", required=False, widget = 
                             forms.TextInput(attrs={'readonly':'readonly','disable':True}))      

    def __unicode__(self):
        return u'%s %s' % (self.id, self.explain)  

    def is_valid(self):
        return super(WordExpForm, self).is_valid()            

    def get_back_array(self, obj):
        array= []
        array.append("phonetic")
        array.append(escape(obj.phonetic))
        array.append("explain")
        array.append(escape(obj.explain))
        array.append("sentence")
        array.append(escape(obj.sentence))        
        array.append("book")
        array.append(escape(obj.book))

        return array

```
这些fields都设为readonly和disable，避免修改

### 定义关联form admin - LinkFormAdmin
``` python
class WordExpLinkFormAdmin(LinkFormAdmin):
    extra = 0
    
    link_form = WordExpForm
    link_obj_class = WordExp
    link_m2m = True
    link_init_search = True
```
link_m2m = True表示这是m2m的关系
link_init_search = True表示这个域初始显示的是搜索图标而不是添加图标

### 配置LinkFrom (admin.py)
``` python
class WordAdmin(MyModelAdmin):
    list_display = ['name','phonetic', 'progress']
    inlines = [
        ExampleWordInline,
        WordDictInline,
    ]

    form_links = [WordExpLinkFormAdmin]

    class Meta:
        model = Word
```
弹出窗口dismiss处理
``` python

```
### 调节列宽 (custom_page.html)
``` javascript
$(document).ready(function() {
{% ifequal opts.object_name.lower "rail_oem_project" %}
        var array_td = ["2%", "13%", "20%", "20%", "10%", "20%"]; //%
        adjust_link_formset("div#rail_bidding_set-group>div>fieldset>table", array_td);

```

### 需完成函数
_save_obj
filter_objects
_delete

linkform exclude  m2m object

字符含换行时，返回页面有问题
