#coding=utf-8 

from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect
import math
from .models import Task, Machine, Option, Launch, LaunchOption
from django.template.context_processors import csrf
import datetime, json
from django.conf import settings

def index(request):
	print "this = " + settings.STATIC_ROOT
	return render(request, 'index.html')

def task(request):
	tasks = Task.objects.all()
	context = {'tasks': tasks}
	return render(request, 'task.html', context)

def machine(request):
	machines = Machine.objects.all()
	context = {'machines': machines}
	return render(request, 'machine.html', context)

def option(request):
	options = Option.objects.all()
	tasks = Task.objects.all()
	context = {'options': options, 'tasks': tasks}
	return render(request, 'option.html', context)

def launch(request):
	launches = Launch.objects.all()
	tasks = Task.objects.all()
	machines = Machine.objects.all()
	context = {'launches': launches, 'tasks': tasks, 'machines': machines}
	return render(request, 'launch.html', context)

def lauopt(request):
	lauopts = LaunchOption.objects.all()
	launches = Launch.objects.all()
	options = Option.objects.all()
	context = {'lauopts': lauopts, 'launches': launches, 'options': options}
	return render(request, 'lauopt.html', context)

def forecasting(request): #FIXME Change context
	launches = Launch.objects.all()
	tasks = Task.objects.all()
	machines = Machine.objects.all()
	options = Option.objects.all()
	context = {'launches': launches, 'tasks': tasks, 'machines': machines, 'options': options}
	return render(request, 'forecast.html', context)

def addtask(request):
	return render(request, 'addtask.html')

def savetask(request, tid):
	title = ""
	if request.method == 'POST':
		title = request.POST['task']
		if len(title) > 0:
			if int(tid) == 0:
				task = Task(Title = title)
				task.save()
			elif int(tid) > 0:
				task = Task.objects.get(id = tid)
				task.Title = title
				task.save()
			return redirect('task')#render(request, 'task.html', context) #HttpResponseRedirect('')
			#else: #show message box
				#return render(request, 'index.html')
		#print "this is savetask"
		#mdict = {'form': form, }
		#mdict.update(csrf(request))

def deletetask(request):
	if request.method == 'POST':
		idtasks = request.POST.getlist('check')
		for tid in idtasks:
			task = Task(id = tid)
			task.delete()
		return redirect('task')

def edittask(request):
	if request.method == 'POST':
		taskid = request.POST.get('check')
		task = Task.objects.get(id = taskid)
		context = {'tasktext': task.Title, 'taskid': taskid}
	return render(request, 'edittask.html', context)

def addmachine(request):
	return render(request, 'addmachine.html')

def savemachine(request, mid):
	if request.method == 'POST':
		noc = request.POST['machinecores']
		if noc > 0:
			if int(mid) == 0:
				mach = Machine(NumOfCores = noc)
				mach.save()
			elif int(mid) > 0:
				mach = Machine.objects.get(id = mid)
				mach.NumOfCores = noc
				mach.save()
			return redirect('machine')

def deletemachine(request):
	if request.method == 'POST':
		idmachs = request.POST.getlist('check')
		for mid in idmachs:
			mach = Machine(id = mid)
			mach.delete()
		return redirect('machine')

def editmachine(request):
	if request.method == 'POST':
		machid = request.POST.get('check')
		mach = Machine.objects.get(id = machid)
		context = {'machid': machid, 'machcores': mach.NumOfCores}
	return render(request, 'editmachine.html', context)

def addoption(request):
	tasks = Task.objects.all()
	context = {'tasks': tasks}
	return render(request, 'addoption.html', context)

def saveoption(request, oid):
	if request.method == 'POST':
		title = request.POST['optionname']
		taskid = request.POST['taskid']
		task = Task.objects.get(id = taskid)
		if int(oid) == 0:
			opt = Option(Title = title, Task = task)
			opt.save()
		elif int(oid) > 0:
			opt = Option.objects.get(id = oid)
			opt.Title = title
			opt.save()
		return redirect('option')

def deleteoption(request):
	if request.method == 'POST':
		idopts = request.POST.getlist('check')
		for oid in idopts:
			opt = Option(id = oid)
			opt.delete()
		return redirect('option')

def editoption(request):
	if request.method == 'POST':
		optid = request.POST.get('check')
		opt = Option.objects.get(id = optid)
		context = {'opt': opt}
	return render(request, 'editoption.html', context)

def addlaunch(request):
	tasks = Task.objects.all()
	machines = Machine.objects.all()
	options = Option.objects.all()
	#optdata = {opt.id: opt.Task.id for opt in options}
	context = {'tasks': tasks, 'machines': machines, 'options': options}
	#print optdata
	#for opt in options:
	#	optdata[opt.id] = opt.Task.id
	return render(request, 'addlaunch.html', context)

def showoptions(request, tid):
	task = Task.objects.get(id = tid)
	options = Option.objects.filter(Task = task)
	oids = {o.id: o.id for o in options}
	return HttpResponse(json.dumps(oids))

def savelaunch(request, lid):
	if request.method == 'POST':
		rtime = request.POST['runtime']
		dsize = request.POST['datasize']
		laudate = request.POST['laudate']
		if int(lid) == 0:
			taskid = request.POST['taskid']
			task = Task.objects.get(id = taskid)
			#date = datetime.datetime.now()
			machid = request.POST['machid']
			mach = Machine.objects.get(id = machid)
			lau = Launch(RunTime = rtime, DataSize = dsize, Date = laudate, Task = task, Machine = mach)
			lau.save()
			options = Option.objects.all()
			for opt in options:
				oidnum = 'oid' + str(opt.id)
				op = request.POST.get(oidnum, False)
				if op != False:
					optname = 'opt' + str(op)
					opvalue = request.POST[optname]
					option = Option.objects.get(id = op)
					laop = LaunchOption(Value = opvalue, Launch = lau, Option = option)
					laop.save()
		elif int(lid) > 0:
			lau = Launch.objects.get(id = lid)
			lau.Date = laudate
			lau.RunTime = rtime
			lau.DataSize = dsize
			lau.save()
			options = Option.objects.all()
			for opt in options:
				oidnum = 'oid' + str(opt.id)
				op = request.POST.get(oidnum, False)
				if op != False:
					optname = 'opt' + str(op)
					opvalue = request.POST[optname]
					option = Option.objects.get(id = op)
					laop = LaunchOption.objects.get(Launch = lau, Option = option)
					laop.Value = opvalue
					laop.save()
		return redirect('launch')

def deletelaunch(request):
	if request.method == 'POST':
		idlaus = request.POST.getlist('check')
		for lid in idlaus:
			lau = Launch(id = lid)
			lau.delete()
		return redirect('launch')

def editlaunch(request):
	if request.method == 'POST':
		lauid = request.POST.get('check')
		lau = Launch.objects.get(id = lauid)
		loptions = LaunchOption.objects.filter(Launch = lau)
		context = {'lau': lau, 'loptions': loptions}
	return render(request, 'editlaunch.html', context)

# def addlauopt(request):
# 	launches = Launch.objects.all()
# 	options = Option.objects.all()
# 	context = {'launches': launches, 'options': options}
# 	return render(request,'addlauopt.html', context)

def savelauopt(request, loid):
 	if request.method == 'POST':
 		value = request.POST['opvalue']
 		#optid = request.POST['optid']
 		#option = Option.objects.get(id = optid)
 		#lauid = request.POST['lauid']
 		#launch = Launch.objects.get(id = lauid)
 		if int(loid) > 0:
	 		laop = LaunchOption.objects.get(id = loid)
	 		laop.Value = value
	 		laop.save()
 		return redirect('lauopt')

# def deletelauopt(request):
# 	if request.method == 'POST':
# 		idlops = request.POST.getlist('check')
# 		for loid in idlops:
# 			laop = LaunchOption(id = loid)
# 			laop.delete()
# 		return redirect('lauopt')

def editlauopt(request):
	if request.method == 'POST':
		laopid = request.POST.get('check')
		laop = LaunchOption.objects.get(id = laopid)
		context = {'laop': laop}
	return render(request, 'editlauopt.html', context)

def funcresult(request):
	if request.method == 'POST':
		numofcores = request.POST['cores']
		options = Option.objects.all()
		maindist = 0
		for opt in options:
			oidnum = 'oid' + str(opt.id)
			op = request.POST.get(oidnum, False)
			if op != False:
				optname = 'opt' + str(op)
				opvalue = request.POST[optname]
				#print opvalue
				maindist = maindist + int(opvalue) * int(opvalue)
		#maindist = math.hypot(float(opt1), float(opt2))
		taskid = request.POST['taskid']
		mach = Machine.objects.filter(NumOfCores = numofcores)
		result = 0.0
		if len(mach) == 0:
			message = "Невозможно рассчитать время работы из-за отсутствия введенного вами значения производительности машины (кол-ва процессоров)."
		else:
			task = Task.objects.get(id = taskid)
			launches = Launch.objects.filter(Machine = mach, Task = task)
			if len(launches) == 0:
				message = 'Задача "' + task.Title.encode('utf-8') + '" не вычислялась на машине с ' + numofcores.encode('utf-8') + ' ядрами.'
			else:
				message = "Полученное время работы: "
				times = [0 for i in range(len(launches))]
				dists = [0 for i in range(len(launches))]

				k = 2 # Метод к-соседей
				index = 0
				for lau in launches:
					lopts = LaunchOption.objects.filter(Launch = lau)
					dist = 0
					for los in lopts:
						dist = dist + math.pow(los.Value, 2)
					dists[index] = math.fabs(maindist - dist)
					times[index] = lau.RunTime
					#weight = 1
					index = index + 1
				mergeSort(dists, times, 0, len(launches) - 1)
				index = 0
				for t in times:
					result = result + t
					index = index + 1
					if index == k:
						break
				#result = result + weight * time
				if index > 0:
					result = result / index
		context = {'message': message, 'resultTime': result}
		return render(request, 'funcresult.html', context)


def mergeSort(d, t, lb=0, ub=-1):
	def merge(d, t, lb, split, ub):
		#Слияние упорядоченных частей массива в буфер temp
		#с дальнейшим переносом содержимого temp в a[lb]...a[ub]

		#текущая позиция чтения из первой последовательности a[lb]...a[split]
		pos1=lb

		#текущая позиция чтения из второй последовательности a[split+1]...a[ub]
		pos2=split+1

		#текущая позиция записи в temp
		pos3=0

		temp = [i for i in xrange(ub-lb+1)]
		tempT = [i for i in xrange(ub-lb+1)]

		#идет слияние, пока есть хоть один элемент в каждой последовательности
		while pos1 <= split and pos2 <= ub:
			if d[pos1] < d[pos2]:
				temp[pos3] = d[pos1]
				tempT[pos3] = t[pos1]
				pos1+=1
				pos3+=1
			else:
				temp[pos3] = d[pos2]
				tempT[pos3] = t[pos2]
				pos2+=1
				pos3+=1

		#одна последовательность закончилась - 
		#копировать остаток другой в конец буфера
		while pos2 <= ub:   #пока вторая последовательность непуста 
			temp[pos3] = d[pos2]
			tempT[pos3] = t[pos2]
			pos3+=1
			pos2+=1
		while pos1 <= split:  #пока первая последовательность непуста
			temp[pos3] = d[pos1]
			tempT[pos3] = t[pos1]
			pos3+=1
			pos1+=1

		#скопировать буфер temp в a[lb]...a[ub]
		d[lb:ub+1] = temp
		t[lb:ub+1] = tempT

		del(temp)
		del(tempT)

	if lb < ub:#если есть более 1 элемента
		split = (lb + ub)/2# индекс, по которому делим массив
		mergeSort(d, t, lb, split)#сортировать левую половину 
		mergeSort(d, t, split+1, ub)#сортировать правую половину 
		merge(d, t, lb, split, ub)#слить результаты в общий массив

# def addtask(request):
# 	checker = True
# 	print "hwgfashgjh"
# 	if request.method == 'POST':
# 		if 'task' not in request.POST:
# 			checker = False
# 		if checker == True:
# 			title = request.POST['task']
# 			tsk = Task(Title=title)
# 			tsk.save()
# 	tasks = Task.objects.all()
# 	context = {'tasks': tasks}
# 	return render('addtask.html',context)