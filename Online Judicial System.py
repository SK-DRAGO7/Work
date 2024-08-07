#==============================================================================
# ONLINE CRIME JUDGMENT SYSTEM
#==============================================================================

#Libraries used
import win32com.client as win32
import nltk
import spacy
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet

#Packages  required
#nltk.download()
#nltk.download("state_union")
#nltk.download("stopwords")
#nltk.download("punkt")
#nltk.download('words')
#nltk.download('wordnet')
#pip install nltk
#pip install spacy
#pip install -U spacy[cuda92]
#conda install -c conda-forge spacy
#python -m spacy download en_core_web_lg
#python -m spacy download en_core_web_sm

def CRIME_SELECTION():
   
    #Reading the word file
    def Read_docx():
        global table
        try:
            word = win32.Dispatch("Word.Application")
            word.Visible = True
            word.Documents.Open(r"C:\Users\SURIYA HAASINI\Desktop\INDIAN PENAL CODE.docx")
            doc = word.ActiveDocument
            table = doc.Tables(1)
            return table
        except AttributeError:
            return None  

    #Tokenizing the sentence
    def Tokenize(case):
        global tokenized_sentence
        tokenized_sentence=word_tokenize(case)
        return tokenized_sentence

    #Tokenizing the document
    def Tokenize_docx():
        global tokenized_docx
        tokenized_docx=[]
        Read_docx()
        for i in range(2,table.Rows.Count+1):
            token=word_tokenize(table.Cell(Row = i,Column = 2).Range.Text)
            tokenized_docx.append(token)
        return tokenized_docx

    #Cleaning the sentence
    def Regexp():
        global dataset
        dataset=tokenized_sentence
        l=len(dataset)
        for i in range(l):
            dataset[i]=dataset[i].lower()
            dataset[i]=re.sub(r"\W"," ",dataset[i])
            dataset[i]=re.sub(r"\s+"," ",dataset[i])
        for j in dataset:
            if j==" ":
                dataset.remove(j)
        return dataset

    #Cleaning the document
    def Regexp_docx():
        global dataset_docx
        Lst=[]
        dataset_docx=[]
        Structure=tokenized_docx
        for i in Structure:
            l1=len(i)
            for j in range(l1):
                i[j]=i[j].lower()
                i[j]=re.sub(r"\W"," ",i[j])
                i[j]=re.sub(r"\s+"," ",i[j])
                Lst.append(i[j])
            for k in Lst:
                for l in k:  
                    if l==" ":
                        Lst.remove(l)
            dataset_docx.append(Lst)
            Lst=[]
        return dataset_docx

    #Removing stop words from the sentence
    def Rem_stop_words():
        global filter
        stop_words=set(stopwords.words("english"))
        filter=[]
        words=dataset
        for i in words:
            if i not in stop_words:
                filter.append(i)
        return filter

    #Removing stop words from the document
    def Rem_stop_words_docx():
        global filter_docx
        filter_docx=[]
        L=[]
        stop_words=set(stopwords.words("english"))
        words_docx=dataset_docx
        for i in words_docx:
            for j in i:
                if j not in stop_words:
                    L.append(j)
            filter_docx.append(L)
            L=[]
        return filter_docx

    #Lemmatizing the sentence
    def Lemmatization():
        global lemmatized
        lemmatized=[]
        lemmatizer=WordNetLemmatizer()
        for i in filter:
            new_words=lemmatizer.lemmatize(i,pos="v")
            lemmatized.append(new_words)
        return lemmatized

    #Lemmatizing the document
    def Lemmatization_docx():
        global lemmatized_docx
        lemmatized_docx=[]
        L=[]
        lemmatizer_docx=WordNetLemmatizer()
        for i in filter_docx:
            for j in i:
                new_words_docx=lemmatizer_docx.lemmatize(j,pos="v")
                L.append(new_words_docx)
            lemmatized_docx.append(L)
            L=[]
        return lemmatized_docx

    #Abstraction of synonyms from the sentence
    def Synonyms():
        global synset
        synset=[]
        syns=[]
        for i in lemmatized:
            for syn in wordnet.synsets(i):
                for s in syn.lemmas():
                    syns.append(s.name())
            synset.append(syns)
            syns=[]
        return synset

    #Abstraction of synonyms from the document
    def Synonyms_docx():
        global synset_docx
        synset_docx=[]
        synms_docx=[]
        syns_docx=[]
        for i in lemmatized_docx:
            for j in i:
                for syn_docx in wordnet.synsets(j):
                    for s in syn_docx.lemmas():
                        syns_docx.append(s.name())
                synms_docx.append(syns_docx)
                syns_docx=[]
            synset_docx.append(synms_docx)
            synms_docx=[]
        return synset_docx

    #Comparing sentence and docx
    def Comparision():
        global compare
        global returned
        compare=[]
        normal=[]
        returned=[]
        sentence=synset
        docx=synset_docx
        l1=len(docx)
        l2=len(sentence)
        for i in range (l1):
            l3=len(docx[i])
            for j in range(l3):
                for k in docx[i][j]:
                    for l in range(l2):
                        for m in sentence[l]:
                            if k==m:
                                compare.append(lemmatized_docx[i])
                                normal.append(table.Cell(Row = i+2,Column = 2).Range.Text)
                                returned.append(normal)
                                normal=[]
        if len(compare)==0:
            return "No matches found"
        else:
            return compare,returned
   
    #Extraction of unique elements
    def Unique_Comparision():
        global unique_compare
        global unique_returned
        unique_compare=[]
        unique_returned=[]
        l1=len(compare)
        l2=len(returned)
        for i in range(l1):
            if compare[i] not in unique_compare:
                unique_compare.append(compare[i])
        for k in range(l2):
            if returned[k] not in unique_returned:
                unique_returned.append(returned[k])
        return unique_compare,unique_returned

    #Finding the similarity ratio
    def Similarity_ratio():
        global percentage
        percentage=[]
        nlp=spacy.load("en_core_web_sm")
        sequence1=lemmatized
        sequence2=unique_compare
        sequence3=" "
        sequence4=" "
        for i in sequence2:
            for j in i:
                sequence3+=j
                sequence3+=" "
                for k in sequence1:
                    while k not in sequence4:
                        sequence4+=k
                        sequence4+=" "
            custom1=nlp(sequence3)
            custom2=nlp(sequence4)
            perc=custom1.similarity(custom2)*100
            percentage.append(perc)
            sequence3=" "
        return percentage

    #Selecting the most appropriate pair    
    def Selection():
        global best_match
        best_match=[]
        smax=max(percentage)
        l=len(unique_returned)
        for i in range(l):
            if percentage[i]==smax:
                best_match.append(unique_returned[i])
        return best_match

    #Converting into string
    def Conversion_1():
        global converted_match
        converted_match=" "
        l=len(best_match)
        for i in range(l):
            for j in best_match[i]:
                converted_match+=j
        return converted_match
   
    #Searching through the document
    def Search1():
        global index
        custom_text= converted_match
        l=table.Rows.Count
        index=0
        for i in range(1,l+1):
            token1=word_tokenize(table.Cell(Row = i,Column = 2).Range.Text)
            token1.pop()
            token2=word_tokenize(custom_text)
            token2.pop()
            if token1==token2:
                index=i
            token1=[]
            token2=[]
        return index
    
    #PRINT STATEMENTS
    #Getting the computer output
    def Computer_Output():
        global satisfaction
        global Punishment1
        Section=table.Cell(Row = index,Column = 1).Range.Text
        Punishment1=table.Cell(Row = index,Column = 3).Range.Text
        Offence=table.Cell(Row = index,Column = 4).Range.Text
        print("Offence selected by the computer:",Offence)
        satisfaction= input("Are you satisfied with the offence selected for this case (Yes/No):")
        if satisfaction=="Yes" or satisfaction=="YES" or satisfaction=="yes" or satisfaction=="Y" or satisfaction=="y":
            print("The court finds the person guilty of the offence:",Offence)
            print("Under IPC",Section)
            print("he/she shall be given the punishment:",Punishment1)
        return satisfaction, Punishment1
   
    #PRINT STATEMENTS
    #Announcing the fine
    def FINE_1():
        if satisfaction=="Yes" or satisfaction=="YES" or satisfaction=="yes" or satisfaction=="Y" or satisfaction=="y":
            if "FINE" in Punishment1:
                if "OR" or "AND" in Punishment1:
                    fine_1=table.Cell(Row = index,Column = 5).Range.Text
                    print("Tne person should pay a fine amount of Rupees",fine_1)
           
    #Searching through the document
    def Manual_Search():
        global options
        s=""
        options1=[]
        options=[]
        while satisfaction=="NO" or satisfaction=="No" or satisfaction=="no" or satisfaction=="N" or satisfaction=="n":
            l=len(unique_returned)
            for h in range(l):
                if percentage[h]>50:
                    options1.append(unique_returned[h])
            if len(options)==0:
                for m in range(l):
                    options1.append(unique_returned[m])
            for i in range(len(options1)):
                for j in options1[i]:
                    s+=j
                options.append(s)
                s=""
            break
        return options
   
    #PRINT STATEMENTS
    #Selecting one option
    def Manual_Selection():
        global selected_option
        selected_option=[]
        select_1=options
        select_2=[]
        pick=True
        print("Related options:")
        l=len(select_1)
        for i in range(l):
            print("Option",i+1,":",select_1[i])
        satisfaction1=input("Did you find any satisfactory option (Yes/No):")
        if satisfaction1=="Yes" or satisfaction1=="YES" or satisfaction1=="yes" or satisfaction=="Y" or satisfaction1=="y":
            ch=int(input("Enter the option number you most preferred for the case:"))
            while pick==True:
                for j in range(l):
                    if ch==j+1:
                        selected_option.append(select_1[j])
                        pick=False
                    elif ch>l or ch<0:
                        print("The option you entered does not match with any of the options given above")
                        print("You need to repick another option")
                        ch=int(input("Enter the option number you most preferred for the case:"))
            return selected_option
        elif satisfaction1=="NO" or satisfaction1=="No" or satisfaction1=="no" or satisfaction1=="N" or satisfaction1=="n":
            print("All options:")
            for k in range (2,table.Rows.Count+1):
                select_2.append(table.Cell(Row = k,Column = 4).Range.Text)
            q=len(select_2)
            for m in range(q):
                print("Option",m+1,":",select_2[m])
            ch=int(input("Enter the option number you most preferred for the case:"))
            while pick==True:
                for n in range(q):
                    if ch==n+1:
                        print(select_2[n])
                        selected_option.append(select_2[n])
                        pick=False
                    elif ch>q or ch<0:
                        print("The option you entered does not match with any of the options given above")
                        print("You need to repick another option")
                        ch=int(input("Enter the option number you most preferred for the case:"))
            return selected_option
    
    #Conversion to string
    def Conversion_2():
        global converted_match2
        converted_match2=" "
        l=len(selected_option)
        for i in range(l):
            for j in selected_option[i]:
               converted_match2+=j
        return converted_match2
       
    #Searching through the document
    def Search2():
        global index2
        custom_text2= converted_match2
        l=table.Rows.Count
        index2=0
        for i in range(1,l+1):
            token1=word_tokenize(table.Cell(Row = i,Column = 2).Range.Text)
            token1.pop()
            token2=word_tokenize(custom_text2)
            token2.pop()
            if token1==token2:
                index2=i
            token1=[]
            token2=[]
        return index2
   
    #PRINT STATEMENTS
    #Getting the manual output
    def Manual_Output():
        global Punishment2
        Section=table.Cell(Row = index2,Column = 1).Range.Text
        Punishment2=table.Cell(Row = index2,Column = 3).Range.Text
        Offence=table.Cell(Row = index2,Column = 2).Range.Text
        print("The court finds the person guilty of the offence:",Offence)
        print("Under IPC",Section)
        print("he/she shall be given the punishment:",Punishment2)
        return Punishment2
     
    #PRINT STATEMENTS
    #Announcing the fine
    def FINE_2():
            if "FINE" in Punishment2:
                if "OR" or "AND" in Punishment2:
                    fine_2=table.Cell(Row = index2,Column = 5).Range.Text
                    print("Tne person should pay a fine amount of Rupees",fine_2)
     
    #PRINT STATEMENTS        
    # MAIN
    case=input("Enter a case:")
    Read_docx()
    Tokenize(case)
    Tokenize_docx()
    Regexp()
    Regexp_docx()
    Rem_stop_words()
    Rem_stop_words_docx()
    Lemmatization()
    Lemmatization_docx()
    Synonyms()
    Synonyms_docx()
    Comparision()
    Unique_Comparision()
    Similarity_ratio()
    Selection()
    Conversion_1()
    Search1()
    Computer_Output()
    FINE_1()
    while satisfaction=="NO" or satisfaction=="No" or satisfaction=="no" or satisfaction=="N" or satisfaction=="n":
        Manual_Search()
        Manual_Selection()
        Conversion_2()
        Search2()
        Manual_Output()
        FINE_2()
        break

CRIME_SELECTION()

#EXAMPLES
#The policeman was bribed by the thief,so he allowed him to escape.
#The politician bribed the people to vote for him during the elections.
