import pytterm 
import json

def correct_lines(ind_list):
    new_indlist = []
    for line in ind_list:
        if '/' in line:
            if 'экспериментов' in line:
                podline = line[0:line.index('экспериментов')]
                new_indlist.append(podline + 'экспериментов')
                new_indlist.append(podline + 'исследования')
            else:
                newl = line.split('/')
                for word in newl:
                    new_indlist.append(word)
        elif '[' in line:
            podline = ''
            if line.index('[') == 0:
                podline = line[line.index(']')+1:]
            else:        
                podline = line[0:line.index('[')]
            new_indlist.append(podline)
            newline = line.replace('[', '')
            newline = newline.replace(']', '')
            new_indlist.append(newline)
        elif '<' in line:
            podline = line[0:line.index('<')]
            new_indlist.append(podline)
            newline = line.replace('<', '')
            newline = newline.replace('>', '')
            new_indlist.append(newline)
        else:
            new_indlist.append(line)
    return new_indlist

def calc_glthesis(target_text, newf, slov_ind_cor, stat_names):
    first_sentence = target_text[0:target_text.index('.')]
    newf.run(first_sentence)
    for key in slov_ind_cor:
        for line in slov_ind_cor[key]:
            fline = 'ind_' + line.replace(' ', '_')
            # if newf[fline] != None:
            if (line.lower() in first_sentence) or (line in first_sentence):
                stat_names[0][3][key] += 1

def calc_stats_in_text(project, textl, stats_in_text):
    for statement in project['data']['statements']:
        stat_val = project['data']['statements'][statement]['val'].lower()
        if stat_val.startswith('s') and ' ' in stat_val:
            stat_val = stat_val[stat_val.index(' ')+1:]
        if stat_val in textl:
            stats_in_text[stat_val] = 0
            for stat in stats_in_text:
                if textl.index(stat_val) > textl.index(stat):
                    stats_in_text[stat_val] += 1
                elif textl.index(stat_val) < textl.index(stat):
                    stats_in_text[stat] += 1

    if stats_in_text.values():
        max_val = max(stats_in_text.values())
        min_val = min(stats_in_text.values())

        for i in range (min_val, max_val):
            if i > max_val:
                break
            while i not in stats_in_text.values():
                for stat in stats_in_text:
                    if stats_in_text[stat] > i:
                        stats_in_text[stat] -= 1
                max_val -= 1

def calc_stat3(line, fline, slovarg, stat_vall, key, stat_names):
    #3
    if 'begin' in slovarg[fline.replace('\n', '')]:
        start = line[:line.index('...')]
        end = line[line.index('...')+3:]
        if stat_vall.startswith(start.lower()) and stat_vall.endswith(end.lower()):
            stat_names[2][0][key] += 1
        else:
            stat_names[2][1][key] += 1
    else:
        if stat_vall.startswith(line.lower()) or stat_vall.endswith(line.lower()):
            stat_names[2][0][key] += 1
        else:
            stat_names[2][1][key] += 1

def add_uri(arg_features, param, param_uri, premise_uri, concl_uri):
    #4
    param_uri.append(arg_features['params'][param]['param'])

    #5
    if 'Premise' in param:
        premise_uri.append(arg_features['params'][param]['param'])
    if 'Conclusion' in param:
        concl_uri.append(arg_features['params'][param]['param'])

def calc_prem_concl(param, key, stat_names):
    if 'Premise' in param:
        stat_names[5][0][key] += 1 #6
    if 'Conclusion' in param:
        stat_names[5][1][key] += 1 #6

def calc_stat2(arg_features, key, stat_names):
    sch_name = arg_features['scheme'][arg_features['scheme'].find('#')+1:]
    if sch_name in stat_names[1][key].keys():
        stat_names[1][key][sch_name] += 1
    else:
        stat_names[1][key][sch_name] = 1

def calc_stat4(uri, param_uri, stats_in_text, key, project, stat_vall, flag_uri, stat_names):
    if uri in param_uri:
        contact_fl = 0
        for ur_val in param_uri:
            if ur_val in project['data']['statements']:
                statement_key = project['data']['statements'][ur_val]['val'].lower()
                if (statement_key in stats_in_text.keys()) and (stats_in_text[stat_vall] - stats_in_text[statement_key] == 1):
                    stat_names[3][0][key] += 1
                    contact_fl = 1
                    break
        if contact_fl == 0 and flag_uri == False:
            stat_names[3][1][key] += 1

def calc_stat5(uri, premise_uri, concl_uri, stats_in_text, key, project, stat_vall, flag_uri, stat_names):
    if (uri in premise_uri) or (uri in concl_uri) :
        l_cntxt_fl = 0
        for ur_val in concl_uri:
            statement_key = project['data']['statements'][ur_val]['val'].lower()
            if (statement_key in stats_in_text.keys()) and (stats_in_text[stat_vall] - stats_in_text[statement_key] == 1):
                stat_names[4][1][key] += 1
                l_cntxt_fl = 1
                break 
        for ur_val in premise_uri:
            statement_key = project['data']['statements'][ur_val]['val'].lower()
            if (statement_key in stats_in_text.keys()) and (stats_in_text[stat_vall] - stats_in_text[statement_key] == 1):
                stat_names[4][0][key] += 1
                l_cntxt_fl = 1
                break
        if l_cntxt_fl == 0 and flag_uri == False:
            stat_names[4][2][key] += 1

def calc_stat1(is_premise, is_conclusion, is_attack, key, stat_names):
    if is_premise and is_conclusion:
        stat_names[0][2][key] += 1
    if is_attack > 0:
        stat_names[0][0][key] += 1
    else:
        stat_names[0][1][key] += 1

def calc_stat7(slov_ind_cor, data, slovarg, newf, stat_names):
    for key in slov_ind_cor:

        stat_names[6][3][key] = 0

        for line in slov_ind_cor[key]:

            fline = 'ind_' + line.replace(' ', '_')

            if 'begin' in slovarg[fline.replace('\n', '')]:
            
                for text in data['texts']:

                    textl = text['text']['content'].lower()
                    newf.run(textl)
                    mid_p = []
                    if newf[fline] != None:

                        for entry in newf[fline]:
                            print(textl[entry.begin():entry.end()])
                            mid_p.append(textl[entry.begin():entry.end()])

                        for project in text['projects']:

                                for statement in project['data']['statements']:
                                    stat_features = project['data']['statements'][statement]
                                    stat_val = stat_features['val']
                                    if stat_val.lower() in mid_p:
                                        uri = stat_features['uri']

                                        for argument in project['data']['arguments']:
                                            arg_features = project['data']['arguments'][argument]

                                            for param in arg_features['params']:
                                                if arg_features['params'][param]['param'] == uri:
                                                    if 'Premise' in param:
                                                        stat_names[6][0][key] += 1
                                                    if 'Conclusion' in param:
                                                        stat_names[6][1][key] += 1
                                    else:
                                        newf.run(stat_val.lower()) 
                                        if newf[fline] != None:
                                            stat_names[6][2][key] += 1
            else:
                stat_names[6][3][key] += 1

def calculate_stats(newf, slovarg, slov_ind_cor, stat_names, num_of_entries, data):

    attack_words = ['Conflict', 'DirectAdHominem_Inference', 'CircumstantialAdHominem_Inference', 'VagueVerbalClassification_Inference', 'ArbitraryVerbalClassification_Inference', 'DirectAdHominem_Inference', 'CircumstantialAdHominem_Inference', 'InconsistentCommitment_Inference', 'Bias_Inference', 'SlipperySlope', 'Dilemma_Inference', 'NegativeConsequences_Inference', 'FalsificationOfHypothesis_Inference', 'ExceptionalCase_Inference', 'Ignorance_Inference', 'EffectToCause_Inference', 'FearAppeal_Inference']
    
    for text in data['texts']:

        #1
        calc_glthesis(text['text']['content'], newf, slov_ind_cor, stat_names)

        textl = text['text']['content'].lower()

        for project in text['projects']:

            stats_in_text = {}
            calc_stats_in_text(project, textl, stats_in_text)

            for statement in project['data']['statements']:
                stat_features = project['data']['statements'][statement]
                stat_val = stat_features['val']
                newf.run(stat_val)

                #4
                
                stat_vall = stat_val.lower()
                if stat_vall.startswith('s') and ' ' in stat_vall:
                    stat_vall = stat_vall[stat_vall.index(' ')+1:]
                
                for key in slov_ind_cor:

                    for line in slov_ind_cor[key]:

                        fline = 'ind_' + line.replace(' ', '_')
                        
                        # if (newf[fline] != None) or (line.lower() in stat_val) or (line in stat_val):
                        if (line.lower() in stat_val) or (line in stat_val):

                            

                            num_of_entries[key] += 1

                            ind_uri = []
                            flag_uri = False

                            calc_stat3(line, fline, slovarg, stat_vall, key, stat_names)
                            
                            uri = stat_features['uri']

                            #1
                            is_attack = 0
                            is_premise = False
                            is_conclusion = False
                            
                            for argument in project['data']['arguments']:

                                #4
                                param_uri = []

                                #5
                                premise_uri = []
                                concl_uri = []

                                arg_features = project['data']['arguments'][argument]
                                for param in arg_features['params']:

                                    add_uri(arg_features, param, param_uri, premise_uri, concl_uri)

                                    if arg_features['params'][param]['param'] == uri:

                                        if uri in ind_uri:
                                            flag_uri = True
                                        else:
                                            ind_uri.append(uri)

                                        calc_prem_concl(param, key, stat_names)

                                        if 'Premise' in param:
                                            is_premise = True #1
                                        if 'Conclusion' in param:
                                            is_conclusion = True #1
                                            
                                        #1
                                        for attack in attack_words:
                                            if attack in arg_features['scheme'][arg_features['scheme'].find('#')+1:] :
                                                is_attack +=1

                                        calc_stat2(arg_features, key, stat_names)
                                      
                                if stat_vall in stats_in_text.keys():
                                    calc_stat4(uri, param_uri, stats_in_text, key, project, stat_vall, flag_uri, stat_names)
                                    calc_stat5(uri, premise_uri, concl_uri, stats_in_text, key, project, stat_vall, flag_uri, stat_names)
                                    
                            #1
                            calc_stat1(is_premise, is_conclusion, is_attack, key, stat_names)       
                            
    calc_stat7(slov_ind_cor, data, slovarg, newf, stat_names)    
                
def get_stats(newg, slov_ind_cor, list_of_stats, num_of_entries):

    slovarg = newg.get_patterns()
    newf = newg.get_finder()

    with open("corpus_nauchpop.json", "r", encoding="utf-8") as f1:
        data1 = json.load(f1)
    with open("corpus_rnf.json", "r", encoding="utf-8") as f2:
        data2 = json.load(f2)

    stat_names = {}

    slov_stats_attack = {}
    slov_stats_support = {}
    mn_arg = {}
    gl_thesis = {}
    stat_names[0] = [slov_stats_attack, slov_stats_support, mn_arg, gl_thesis]

    schemas = {}
    stat_names[1] = schemas

    is_segment = {}
    not_segment = {}
    stat_names[2] = [is_segment, not_segment]

    contact = {}
    no_contact = {}
    stat_names[3] = [contact, no_contact]

    prem_l = {}
    concl_l = {}
    nothing = {}
    stat_names[4] = [prem_l, concl_l, nothing]

    prem_r = {}
    concl_r = {}
    stat_names[5] = [prem_r, concl_r]

    prem_m = {}
    concl_m = {}
    no_stat = {}
    not_razr = {}
    stat_names[6] = [prem_m, concl_m, no_stat, not_razr]

    

    for key in slov_ind_cor:
        for st_key in stat_names:
            if st_key != 1:
                for stat in stat_names[st_key]:
                    stat[key] = 0
            else:
                stat_names[1][key] = {}

        num_of_entries[key] = 0

    calculate_stats(newf, slovarg, slov_ind_cor, stat_names, num_of_entries, data1)
    for corpora in data1['subcorpora']:
        calculate_stats(newf, slovarg, slov_ind_cor, stat_names, num_of_entries, corpora)

    for corpora in data2['subcorpora']:
        calculate_stats(newf, slovarg, slov_ind_cor, stat_names, num_of_entries, corpora)

    for key in slov_ind_cor:
        
        for stat in list_of_stats:
            stat[key] = ''

        yasno = 0
        if slov_stats_support[key] > 0:
            list_of_stats[0][key] += 'Поддержка: ' + str(slov_stats_support[key]) + ' вхождений. Процент вхождений: ' + str(slov_stats_support[key]/ num_of_entries[key] * 100) + '%\n'
            yasno = 1
        if slov_stats_attack[key] > 0:
            list_of_stats[0][key] += 'Атака: ' + str(slov_stats_attack[key]) + ' вхождений. Процент вхождений: ' + str(slov_stats_attack[key]/ num_of_entries[key] * 100) + '%\n'
            yasno = 1
        if mn_arg[key] > 0:
            list_of_stats[0][key] += 'Множественная аргументация: ' + str(mn_arg[key]) + ' вхождений. Процент вхождений: ' + str(mn_arg[key]/ num_of_entries[key] * 100) + '%\n'
            yasno = 1
        if gl_thesis[key] > 0:
            list_of_stats[0][key] += 'Главный тезис: ' + str(gl_thesis[key]) + ' вхождений\n'
            yasno = 1
        if yasno == 0:
            list_of_stats[0][key] = 'Неясно\n'

        for schem in schemas[key]:
            list_of_stats[1][key] += schem + ': ' + str(schemas[key][schem]) + ' вхождений. Процент вхождений: ' + str(schemas[key][schem]/ num_of_entries[key] * 100) + '%\n'

        if is_segment[key] > 0:
            list_of_stats[2][key] += 'Сегментирующий: ' + str(is_segment[key]) + ' вхождений. Процент вхождений: ' + str(is_segment[key]/ num_of_entries[key] * 100) + '%\n'
        if not_segment[key] > 0:
            list_of_stats[2][key] += 'Несегментирующий: ' + str(not_segment[key]) + ' вхождений. Процент вхождений: ' + str(not_segment[key]/ num_of_entries[key] * 100) + '%\n'
        if (is_segment[key] > 0) and (not_segment[key] > is_segment[key]):
            list_of_stats[2][key] += 'Иногда сегментирующий\n'

        if contact[key] > 0:
            list_of_stats[3][key] += 'Контактность слева: ' + str(contact[key]) + ' вхождений. Процент вхождений: ' + str(contact[key]/ num_of_entries[key] * 100) + '%\n'
        if no_contact[key] > 0:
            list_of_stats[3][key] += 'Нет контактности слева ' + str(no_contact[key]) + ' вхождений. Процент вхождений: ' + str(no_contact[key]/ num_of_entries[key] * 100) + '%\n'

        if prem_l[key] > 0:
            list_of_stats[4][key] += 'Premise: ' + str(prem_l[key]) + ' вхождений. Процент вхождений: ' + str(prem_l[key]/ num_of_entries[key] * 100) + '%\n'
        if concl_l[key] > 0:
            list_of_stats[4][key] += 'Conclusion: ' + str(concl_l[key]) + ' вхождений. Процент вхождений: ' + str(concl_l[key]/ num_of_entries[key] * 100) + '%\n'
        if nothing[key] > 0:
            list_of_stats[4][key] += 'Ничего: ' + str(nothing[key]) + ' вхождений. Процент вхождений: ' + str(nothing[key]/ num_of_entries[key] * 100) + '%\n'

        if prem_r[key] > 0:
            list_of_stats[5][key] += 'Premise: ' + str(prem_r[key]) + ' вхождений. Процент вхождений: ' + str(prem_r[key]/ num_of_entries[key] * 100) + '%\n'
        if concl_r[key] > 0:
            list_of_stats[5][key] += 'Conclusion: ' + str(concl_r[key]) + ' вхождений. Процент вхождений: ' + str(concl_r[key]/ num_of_entries[key] * 100) + '%\n'

        if prem_m[key] > 0:
            list_of_stats[6][key] += 'Premise: ' + str(prem_m[key]) + ' вхождений. Процент вхождений: ' + str(prem_m[key]/ num_of_entries[key] * 100) + '%\n'
        if concl_m[key] > 0:
            list_of_stats[6][key] += 'Conclusion: ' + str(concl_m[key]) + ' вхождений. Процент вхождений: ' + str(concl_m[key]/ num_of_entries[key] * 100) + '%\n'
        if no_stat[key] > 0:
            list_of_stats[6][key] += 'Нет утверждения: ' + str(no_stat[key]) + ' вхождений. Процент вхождений: ' + str(no_stat[key]/ num_of_entries[key] * 100) + '%\n'
        if not_razr[key] == len(slov_ind_cor[key]):
            list_of_stats[6][key] += 'Нет разрывных индикаторов\n'

def print_stats(list_of_stats, slov_ind, num_of_entries):

    f_res = open('res_stats.txt', 'w', encoding='utf-8')

    for key in slov_ind:

        if num_of_entries[key] != 0:
            f_res.write('\n\n\nИндикаторы:\n')
            for line in slov_ind[key]:
                f_res.write(line)

            f_res.write('\nСтатистика по индикаторам:\n')
            f_res.write('Общее количество вхождений: '+ str(num_of_entries[key]) + '\n')
            for i in range (7):
                if list_of_stats[i][key] != '':
                    f_res.write('Информация по пункту '+ str(i+1) + ':\n')
                    f_res.write(list_of_stats[i][key])
                    f_res.write('\n')

def do_main_stats():
    f_ind = open('indic.txt', 'r', encoding='utf-8')
    count = 1
    name_of_key = 'ind_' + str(count)

    slov_ind = {name_of_key:[]}
    slov_ind_cor = {name_of_key: []}
    for line in f_ind:
        if count == 1:
            slov_ind_cor[name_of_key] = correct_lines(slov_ind[name_of_key])
        if line == '\n':
            slov_ind_cor[name_of_key] = correct_lines(slov_ind[name_of_key])
            count += 1
            new_ind = []
            name_of_key = 'ind_' + str(count)
            slov_ind[name_of_key] = new_ind
            slov_ind_cor[name_of_key] = new_ind
        else:
            slov_ind[name_of_key].append(line)

    newg = pytterm.get_generator()
    for name_of_key in slov_ind_cor:
        for line in slov_ind_cor[name_of_key]:
            line = line.replace('\n', '')
            if '...' in line:
                newg.add_example('ind_' + line.replace(' ', '_'), line.split('...'))
            else:
                newg.add_example('ind_' + line.replace(' ', '_'), [line])

    list_of_stats = []
    for i in range (7):
        list_of_stats.append({})

    num_of_entries = {}

    get_stats(newg, slov_ind_cor, list_of_stats, num_of_entries)
    print_stats(list_of_stats, slov_ind, num_of_entries)


#main

print(''''
      Данная программа считает количество вхождений индикаторов в файле indic.txt в текстах из Научно-популярного корпуса 
      и Научного корпуса РНФ по следующим пунктам:\n
      1. Тип отношения: поддержка (1) / атака (-1) / множественная поддержка (2) / множественная аргументация (3) / главный тезис (4) / неясно (0)\n
         Индикатор считается атакующим, если он находится в схемах аргументации разделов "Conflict" и "Направление атаки"\n
         Индикатор считается поддерживающим, если он не находится в схемах аргументации разделов "Conflict" и "Направление атаки"\n
         Индикатор является множественной аргументацией, если для одного и того же утверждения он находится и в посылке, и заключении\n
         Индикатор находится в главном тезисе, если он находится в первом предложении текста\n
      2. Схема или класс схем \n
      3. Сегментирующий (да (1 - по умол) / нет (0) / иногда (-1) / сам индикатор (2) - сегмент)\n
         Если индикатор разрывный, то он сегментирующий тогда, когда он находится на обеих границах утверждения\n
         Если индикатор неразрывный, то он сегментирующий тогда, когда он находится на одной из границ утверждения\n
         Индикатор иногда сегментирующий, если несегментирующих вхождений больше, чем сегментирующих \n
      4. Обязательность контактности (для роли слева) ( да (1 - по умол) / нет (0) )\n
         Если ближайшее утверждение слева находится в той же схеме аргументации, что и индикатор, то индикатор контактный\n
      5. Роль слева: <название_роли> /Premis (1) / Conl (2) / ничего (0)\n 
         Если ближайшее утверждение слева находится в той же схеме аргументации, что и индикатор, то смотрим, является ли оно посылкой или заключением\n
      6. Собственный контекст = роль справа: <название_роли> /Premis (1) / Conl (2) \n
         Смотрим, является ли утверждение с индикатором посылкой или заключением\n
      7. В разрыве: <название_роли> /Premis (1) / Conl (2) / 0-нет самостоятельно значимого утв\n
         Смотрим на утверждение, стоящее в разрыве между двумя частями разрывного индикатора \n
      ''')

do_main_stats()

print('Вся информация находится в файле res_stats.txt')
