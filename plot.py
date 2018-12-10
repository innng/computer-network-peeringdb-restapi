from statsmodels.distributions.empirical_distribution import ECDF
from matplotlib import pyplot as plt
import pandas as pd


def main():
    df = pd.read_csv('analise1.csv', sep='\t', names=['id', 'name', 'count'])
    plotECDF(df['count'], filename='plot1.png')


def plotECDF(data, scale_x="linear", scale_y="linear", filename=None):
    ecdf = ECDF(data)
    x, y = ecdf.x, ecdf.y
    fig = plt.figure()
    plt.plot(x, y, '.-', color='orange')
    plt.ylabel("CDF(#redes)")
    plt.xlabel("#redes")
    plt.xscale(scale_x)
    plt.yscale(scale_y)
    plt.title('CDF #Redes por IXP')
    if filename:
        fig.savefig(filename, dpi=150)


if __name__ == '__main__':
    main()
