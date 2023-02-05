import pandas as pd
import random
from faker import Faker
from dataclasses import dataclass, asdict
from faker.providers import BaseProvider
from typing import List
import json

Faker.seed(4321)
fake = Faker()
random.seed(4321)


@dataclass(frozen=True)
class ShieldItem:
    shield_path: str
    shield_type: str
    remark: str


@dataclass(frozen=True)
class RemapItem:
    target_pattern: str
    replacement: str
    remark: str


def fake_baseline(n):
    res = set()
    for _ in range(n):
        fp = fake.unique.file_path(depth=4, absolute=False, category='text', extension='c')
        res.add(fp)
    return list(res)


def fake_target(baseline):
    l = baseline[:]
    mid = len(l) // 2
    random.shuffle(l)
    scanned, missed = l[:mid], l[mid:]
    return scanned, missed




def fake_shield(missed):
    shields = []
    for fp in missed[:5]:
        shield = { 
            'shield_path': fp,
            'shield_type': 'file',
            'remark': fake.text(50)
        }
        shields.append(shield)
    
    dir_name1 = 'test_sheild_dir/test/a_dir'
    dir_name2 = 'test_sheild_dir/test_b'


    shield_1 = { 
        'shield_path': dir_name1,
        'shield_type': 'dir',
        'remark': fake.text(30)
    }

    shield_2 = { 
        'shield_path': dir_name2,
        'shield_type': 'dir',
        'remark': fake.text(30)
    }

    shields.append(shield_1)
    shields.append(shield_2)

    for _ in range(5):
        fp1 = f'{dir_name1}/{fake.file_path(depth=3, absolute=False)}'
        fp2 = f'{dir_name2}/{fake.file_path(depth=3, absolute=False)}'
        missed.append(fp1)
        missed.append(fp2)

    return shields


def save_filepaths(fns: List[str], output: str):
    res = [{'file_name': fn} for fn in fns]
    save_obj(res, output)

def save_obj(obj, output: str):
    with open(output, mode='w') as fp:
        json.dump(obj, fp, indent=4)


if __name__ == '__main__':
    baseline = fake_baseline(30)
    target, missed = fake_target(baseline)
    shield = fake_shield(missed)
    save_filepaths(baseline, 'baseline.json')
    save_filepaths(target, 'target.json')
    save_filepaths(missed, 'missed.json')
    save_obj(shield, 'shield.json')


