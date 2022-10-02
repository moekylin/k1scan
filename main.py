import api
import save
from poc import PocCheck
from tqdm import tqdm
import threading
from threading import Thread


def get_thread(target, args):
    t = (Thread(target=target, args=(args,)))
    t.start()
    t.join()


while True:
    print("""
[1] FOFA数据采集
[2] POC 批量检测
[3] 爱站-权重查询 (未实现)
[4] 数据合并/去重
""")

    option = input('请输入选项 1/2/3/4: ')
    # FOFA 数据采集模块
    if option == '1':
        fofa_rules = input('请输入 FOFA 规则语句: ')
        fofa_results = api.fofa(fofa_rules)
        save_opt = input('是否保存数据?[y/N]:')
        if save_opt in ['N', 'n', 'no', 'NO']:
            break
        elif save_opt in ['Y', 'y', 'yes', 'YES']:
            save.output(fofa_results)
            break
    # POC 批量检测模块
    if option == '2':
        poc_check_file = input('请将文件放在 results 目录下, 并输入文件名称: ')
        try:
            with open(f'./results/{poc_check_file}') as f:
                hit_url = []
                # for url in tqdm(f.read().splitlines()):
                print('=== [以下为命中结果] ===')
                for url in f.read().splitlines():
                    # 处理主机头
                    if 'http://' not in url:
                        url = 'http://' + url
                    runner = PocCheck()
                    # 多线程调用
                    get_thread(runner.run_test, url)
                    # 单线程调用
                    # url = runner.run_test(url=url)
                    # 如果命中则导入数组
                    if url:
                        hit_url.append(url)
                # print(f'共有 [{len(hit_url)}] 个命中结果')
        except Exception as e:
            print(e)
    # 数据合并/去重
    if option == '4':
        print('将对 results 内所有结果进行排序去重')
        screening = input('是否进行操作?[y/N]:')
        if screening in ['N', 'n', 'no', 'NO']:
            break
        elif screening in ['Y', 'y', 'yes', 'YES']:
            new_filename = input('输入保存的新文件名: :')
            save.merge_dedup('results/', new_filename)
            break
