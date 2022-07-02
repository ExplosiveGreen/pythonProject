from bs4 import BeautifulSoup
import requests
import matplotlib.pyplot as plt
import re
jobs=['Software_Engineer','Senior_Software_Engineer','Full_Stack_Software_Developer','Web_Developer','Senior_Web_Developer','Development_Operations_(DevOps)_Engineer','Senior_Development_Operations_(DevOps)_Engineer']
Experience=['Entry Level','Early Career','Mid Career','Experienced','Late Career']
def show_all_jobs():
    salarys=list()
    for id,job in enumerate(jobs):
        salary=get_job(job)
        salarys.append(dict())
        for key,val in salary.items():
            _,avg,_=val
            l=list()
            l.append(avg)
            salarys[id][key]=l

    plot(list(i+"(avg)" for i in jobs),salarys)
    return {"result":{
            "labels":list(i+"(avg)" for i in jobs),
            "values":salarys
    }}
def show_job_graph(job=None,c=None):
    if not job:
        print(f"Enter job from list:{jobs}")
        job = input()
    index=-1
    for id,jb in enumerate(jobs):
        if jb == job:
            index=id
            break
    if index == -1:
        print("job not in list try again")
        main()
    else :
        if not c:
            print("Enter 1 for low graph 2 for avg graph 3 for high graph or 4 for all")
            c=int(input())
        else:
            c=int(c)
        l=list()
        if c>5 or c<1:
            print("wrong input")
            main()
        if c==4:
            l.append(get_job(jobs[index]))
            plot([jobs[index]+'(low)', jobs[index]+'(avg)', jobs[index]+'(high)'], l)
        else:
            salary=dict()
            for key,val in get_job(jobs[index]).items():
                low,avg,high=val
                v=-1
                name=""
                if c==1:
                    v=low
                    name='(low)'
                elif c==2:
                    v=avg
                    name='(avg)'
                elif c==3:
                    v=high
                    name='(high)'
                salary[key]=[v]
            l.append(salary)
            print(l)
            plot([jobs[index]+name],l)
            return {"result":{
                "labels":[jobs[index]+name],
                "values":l
            }}
def show_job_skill(job=None,skill=None,c=None):
    if not job:
        print(f"Enter job from list:{jobs}")
        job = input()
    index = -1
    for id, jb in enumerate(jobs):
        if jb == job:
            index = id
            break
    if index == -1:
        print("job not in list try again")
        main()
    else:
        if not skill:
            l,lb=get_job_skill(jobs[index])
            print(f"Enter skill from list:{lb}")
            skill=input()
        salary=list()
        index2=-1
        for i,b in enumerate(lb):
            if b==skill:
                index2=i
                break
        if index==-1:
            print("skill not in list try again")
            main()
        if not c:
            print("Enter 1 for low graph 2 for avg graph 3 for high graph or 4 for all")
            c = int(input())
        else:
            c = int(c)
        if c>5 or c<1:
            print("wrong input")
            main()
        elif c==4:
            salary.append(l[index2])
            plot([jobs[index]+'(low)', jobs[index]+'(avg)', jobs[index]+'(high)'], salary)
        else:
            salary.append(dict())
            for key,val in l[index2].items():
                low,avg,high=val
                v=-1
                name=""
                if c==1:
                    v=low
                    name="(low)"
                elif c==2:
                    v=avg
                    name="(avg)"
                elif c==3:
                    v=high
                    name="(high)"
                lll=list()
                lll.append(v)
                salary[0][key]=lll
            plot([lb[index2]+name], salary)
            return {"result":{
                "labels":[lb[index2]+name],
                "values":salary
            }}
def show_jobs_skills(job=None):
    if not job:
        print(f"Enter job from list:{jobs}")
        job = input()
    index = -1
    for id, jb in enumerate(jobs):
        if jb == job:
            index = id
            break
    if index == -1:
        print("job not in list try again")
        main()
    else:
        l,lb=get_job_skill(jobs[index])
        salary=list()
        for index1,ll in enumerate(l):
            salary.append(dict())
            for key,val in ll.items():
                _,avg,_=val
                lll=list()
                lll.append(avg)
                salary[index1][key]=lll

        plot(list(b+"(avg)" for b in lb), salary)
        return {"result":{
            "labels":list(b+"(avg)" for b in lb),
            "values":salary
        }}
def get_job_skill(job):
    salary = list()
    labels=list()
    html = requests.get(f"https://www.payscale.com/research/IL/Job={job}/Skill")
    soup = BeautifulSoup(html.text, 'html.parser')
    context = soup.find_all('div', {'class': 'subdirectory-links__link'})
    if context:
        for div in context:
            aa=div.find('a')
            salary.append(get_jobs(f"https://www.payscale.com{aa.attrs['href']}"))
            labels.append(aa.text)
    return salary,labels
def get_jobs(url):
    salary = dict()
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'html.parser')
    context = soup.find('div', {'class': 'dropdowns__dropdown--experience'})
    if context:
        a = context.find_all('a')[:-1]
        for aa in a:
            level = aa.text
            html = requests.get(f"https://www.payscale.com{aa.attrs['href']}")
            soup1 = BeautifulSoup(html.text, 'html.parser')
            salary[level] = get_value(soup1)
    else:
        salary[Experience[0]] = get_value(soup)
    return salary
def get_job(job):
    return get_jobs(f"https://www.payscale.com/research/IL/Job={job}/Salary")
def get_value(soup):
    info = soup.find_all('div', {'class': 'percentile-chart__label'})
    if info:
        val = list()
        for div in info:
            if len(div.find_all("div"))==2:
                di = div.find_all("div")[1:]
                val.append(di[0].text)
        return (moneyToNumber(val[0]), moneyToNumber(val[1]), moneyToNumber(val[2]))
    else:
        info = soup.find('span', {'class': 'paycharts__value'})
        return (moneyToNumber(info.text), moneyToNumber(info.text), moneyToNumber(info.text))
def plot(labels,values):
    plt.xlabel("Experience")
    plt.ylabel("Salary")
    plt.title("Salary graph")
    x=list()
    y=list()
    index=-1
    for v in values:
        if len(values)>1:
            x.append(list())
            index+=1
            y.append(list())
        else:
            x.append(list())
        for key,val in v.items():
            if len(values) == 1:
                index = 0
            for id,ex in enumerate(Experience):
                if  key == ex:
                    if id==0:
                        x[index].append(0)
                    elif id==1:
                        x[index].append(1)
                    elif id==2:
                        x[index].append(5)
                    elif id==3:
                        x[index].append(10)
                    elif id == 4:
                        x[index].append(20)
                    for key,val1 in enumerate(val):
                        if len(values)==1:
                            if len(y)<len(labels):y.append(list())
                        y[index].append(val1)
                        if len(values)==1:
                            index+=1
                    break
    if len(values) == 1:x=x*3
    for id,yy in enumerate(y):
        plt.plot(x[id], yy, '-o', label=labels[id])
def moneyToNumber(money):
    regex=re.compile('[^0-9]')
    return int(regex.sub('',money))*(1000 if 'k' in money else 1)
def main():
    while True:
        print("Enter  | for\n"
              "   1   | getting specific job salary \n"
              "   2   | getting specific job average salary by skill\n"
              "   3   | getting all jobs average salary\n"
              "   4   | show specific job with a specific skill salary\n"
              "   5   | show graph\n"
              "  -1   | for exiting the program\n")
        choice=int(input())
        if choice==1:
            show_job_graph()
        elif choice==2:
            show_jobs_skills()
        elif choice==3:
            show_all_jobs()
        elif choice==4:
            show_job_skill()
        elif choice==5:
            plt.legend()
            plt.show()
        elif choice==-1:
            exit(0)

if __name__=='__main__':
    main()
