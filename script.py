
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