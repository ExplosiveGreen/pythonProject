import numpy as np

values = list(map(float, '''-18.11,	28.71,	18.4,	31.49,	-4.38,	21.83,	11.96,	1.38,	13.69,	32.39,	16,	2.11,	15.06,	26.46,
	-37,	5.49,	15.79,	4.91,	10.88,	28.68,	-22.1,	-11.89,	-9.1,	21.04,	28.58,	33.36,	22.96,	37.58,	1.32,	
	10.08,	7.62,	30.47,	-3.1,	31.69,	16.61,	5.25,	18.67,	31.73,	6.27,	22.56,	21.55,	-4.91,	32.42,	18.44,	
	6.56,	-7.18,	23.84,	37.2,	-26.47,	-14.66,	18.98,	14.31,	4.01,	-8.5,	11.06,	23.98,	-10.06,	12.45,	16.48,	
	22.8,	-8.73,	26.89,	0.47,	11.96,	43.36,	-10.78,	6.56,	31.56,	52.62,	-0.99,	18.37,	24.02,	31.71,	18.79,	
	5.5,	5.71,	-8.07,	36.44,	19.75,	25.9,	20.34,	-11.59,	-9.78,	-0.41,	31.12,	-35.03,	33.92,	47.67,	-1.44,	
	53.99,	-8.19,	-43.34,	-24.9,	-8.42,	43.61,	37.49,	11.62'''.strip(' ').split(',')))
values.reverse()


def main():

    Xfunc = np.prod([((1 + values[i] / (100 * 12)) ** 12) for i in range(0, len(values))])
    Payfunc = -20_000 * sum([
        (sum([
            (
                    (1 + 0.05 * i + 0.05 * j / 12) *
                    (1 + values[i] / (100 * 12)) ** (13 - j) *
                    np.prod([
                        ((1 + values[k] / (100 * 12)) ** 12)
                        for k in range(i + 1, len(values))
                    ])
            )
            for j in range(1, 12)
        ]))
        for i in range(0, len(values))
    ])
    futureX = 1.05 ** len(values)
    print(f'{Xfunc}x{Payfunc} = {futureX}x')
    print(f'{Xfunc}x{-futureX}x = {-Payfunc}')
    print(f'{Xfunc-futureX}x = {-Payfunc}')
    print(f'x = {-Payfunc/(Xfunc - futureX)}')

    print("Simulation")
    x = 5_803_530
    x_after = x * 1.05**len(values)
    for year, value in enumerate(values):
        month_profit = (1+value/100) ** (1/12)
        month_inflation = 1.05 ** (1/12)
        print (f"x = {x}, month_profit = {month_profit}, month_inflation = {month_inflation}")
        for month in range(12):
            x = (x - (20_000 * (year*0.05 + month_inflation))) * month_profit
    print(f"{x} =? {x_after}")



if __name__ == '__main__':
    main()
