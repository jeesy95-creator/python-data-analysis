import numpy as np
from matplotlib import pyplot as plt
from scipy import stats

A = np.random.normal(50,10,100)
B = np.random.normal(55,10,100)

mean_A = np.mean(A)
mean_B = np.mean(B)

t_stat, p_value = stats.ttest_ind(A, B)

print(f"A 평균 효과: {mean_A:.3f}")
print(f"B 평균 효과: {mean_B:.3f}")
print(f"t-검정 통계량: {t_stat:.3f}")
print(f"p-값: {p_value:.3f}")

# t-검정의 p-값 확인 (위 예시에서 계산된 p-값 사용)
print(f"p-값: {p_value:.3f}")
if p_value < 0.05:
    print("귀무가설을 기각합니다. 통계적으로 유의미한 차이가 있습니다.")
else:
    print("귀무가설을 기각하지 않습니다. 통계적으로 유의미한 차이가 없습니다.")
