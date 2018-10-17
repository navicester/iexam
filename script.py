
# automatically add Word from WordExp
import os
os.getcwd()

filename = "test.txt"

def get_name_list_from_file(filename):
    from engdict.models import WordExp, Word
    words = []      
    with open(filename, "r") as f:
        for line in f.readlines():
            # print line
            words.append(line.strip('\n'))
    # print words
    return words

def get_wordexp_list_from_file(filename):
    result = []
    for word in get_name_list_from_file(filename):
        for _ in WordExp.objects.filter(name=word):
            result.append(_)
    return result


def read_wordexp_from_file(filename):
    for word in get_name_list_from_file(filename):
        try:
            # print ins
            ins = WordExp.objects.filter(name=word)
            if ins and len(ins):
                getins = ins[0]
                if not Word.objects.filter(name=word).count():
                    print "{} to be created".format(word)
                    new_word = Word(name=word, book=getins.book, explain=getins.explain)
                    new_word.save()
                    print "{} created".format(word)
                else:                
                    print "{} already exist".format(word)
            else:
                print "{} not exist".format(word)
                print ins
        except:
            print "exception for {}".format(word)

# add WordExp and Word relationship if same name

list_wordexp_for_link = WordExp.objects.all()
list_wordexp_for_link = get_wordexp_list_from_file("test.txt")
print list_wordexp_for_link


def add_relationship_for_wordexp_word(list_wordexp_for_link):
    from engdict.models import WordExp, Word
    for object in list_wordexp_for_link:
        name = object.name
        try:
            ins = Word.objects.get(name=name)
        except:
            ins = None
            print "{} not exist".format(name)   
        if not ins:
            continue    
        if not object in ins.wordexp.all():
            ins.wordexp.add(object)

from engdict.models import WordExp, Word
def migrate_exist_specific_type_related_for_word_throught_wordexp(name, name2):
    for word in Word.objects.all():
        for wordexp in getattr(word,name).all():
            word_related = Word.objects.filter(name=wordexp.name)
            if word_related and len(word_related):                
                word_related_obj = word_related[0]
                print "come on {} {}".format(word.name, word_related_obj.name)
                if not (word_related_obj in getattr(word,name2).all()):
                    print "a ha {}".format(word.name)
                    getattr(word,name2).add(word_related_obj)
                    getattr(word_related_obj,name2).add(word)

migrate_exist_specific_type_related_for_word_throught_wordexp('etyma', 'etyma_word')                    
migrate_exist_specific_type_related_for_word_throught_wordexp('resemblance', 'resemblance_word') 
migrate_exist_specific_type_related_for_word_throught_wordexp('semantic', 'semantic_word') 
migrate_exist_specific_type_related_for_word_throught_wordexp('antonymy', 'antonymy_word') 