import numpy as np
import matplotlib.pyplot as plt

h264Idx=[0,1,1,0,1,1,0,0,1,1,0]
hevcIdx=[[1,0,0,1,0,0,1,1,0,0,1],
         [0,1,1,0,0,1,1,0,1,1,0]]
vp9Idx=[[1,0,0,1,0,0,1,1,0,0,1],
        [1,0,0,1,1,0,0,1,0,0,1]]


def get_scores(stats, fileIdx, codecIdx):
    if codecIdx == 0: # h264, sessions 0 and 1
        scores0 = stats[0][fileIdx][h264Idx[fileIdx]]
        scores1 = stats[1][fileIdx][h264Idx[fileIdx]]
    elif codecIdx == 1:
        # hevc
        scores0 = stats[1][fileIdx][hevcIdx[0][fileIdx]]
        scores1 = stats[2][fileIdx][hevcIdx[1][fileIdx]]
    elif codecIdx == 2: # vp9
        scores0 = stats[0][fileIdx][vp9Idx[0][fileIdx]]
        scores1 = stats[2][fileIdx][vp9Idx[1][fileIdx]]
    else:
        raise Exception('codec idx in range 0-2')

    scores = scores0 + scores1
    return scores


def get_average_by_codec(stats):
    avgstats = [[ [] for _ in range(3)] for _ in range(11)]
    for idx, file in enumerate(stats):
        for idx2, codec in enumerate(file):
            mean_codec = np.mean(codec)
            avgstats[idx][idx2] = mean_codec

    npstats = np.asarray(avgstats)
    avcodec = np.mean(npstats, axis=0)

    return avcodec


def collect_points(files, filesDir):

    stats = [ [ [ [] for _ in range(2)  ] for _ in range(11)] for _ in range(3)]

    for file in files:

        with open(filesDir+file, 'r') as f:
            contents = f.read().splitlines()

        for line in contents:
            elems = line.split(' ')

            session = int(elems[0])
            expr = int(elems[1])
            T1 = int(elems[2])
            T2 = int(elems[3])

            stats[session-1][expr-1][0].append(T1)
            stats[session-1][expr-1][1].append(T2)

    return stats


def get_stats_by_file(stats):
    stats2 = [[ [] for _ in range(3)] for _ in range(11)]

    for fileIdx in range(11):
        for codecIdx in range(3):
            scores = get_scores(stats, fileIdx, codecIdx)
            stats2[fileIdx][codecIdx] = scores
    return stats2


def main():
    _filesDir = './data/'
    _files = ('2015','2016','2017')

    _stats = collect_points(_files, _filesDir)
    fstats = get_stats_by_file(_stats)

    plt.rcParams.update({'font.size': 22})

    import dataset
    vids = dataset.load_videos()
    for idx, file in enumerate(fstats):
        plt.figure()
        plt.ylabel('Opinion Score')
        title = vids[idx]['show']
        plt.title(title)
        bp = plt.boxplot(file,
                         labels= ('H264', 'HEVC', 'VP9')
                         )
        plt.savefig(title+'.png')

if __name__ == '__main__':
    main()
