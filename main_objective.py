import os
import dataset
import encode
import time
import numpy as np

videos = dataset.load_videos()
encodeDir = './out/encoded/'
logDir = './out/logs/'

os.makedirs(encodeDir, exist_ok=True)
os.makedirs(logDir, exist_ok=True)

bitrates = range(256,9*256+1,256)

# 1. Encode videos
times = open('./out/encoding_times.txt', 'w')

for rate in bitrates:
    for video in videos:
        times.write(video['show'] + ' ' + str(rate) + 'kbps\n')

        tic = time.time()
        encode.encode_h264(video, bitrate=str(rate),
                           outputFile=os.path.join(encodeDir, video['fname']+ '_' + str(rate) + '.mp4'),
                           logFile=os.path.join(logDir, 'log_'+video['fname']+'_h264_' + str(rate)))
        toc = time.time()
        times.write(str(toc-tic) + '\n'), times.flush()

        tic = time.time()
        encode.encode_h265(video, bitrate=str(rate),
                           outputFile=os.path.join(encodeDir, video['fname']+ '_' + str(rate) + '.265'),
                           logFile=os.path.join(logDir, 'log_'+video['fname']+'_h265_' + str(rate)))
        toc = time.time()
        times.write(str(toc - tic) + '\n'), times.flush()

        tic = time.time()
        encode.encode_vp9(video, bitrate=str(rate),
                           outputFile=os.path.join(encodeDir, video['fname'] + '_' + str(rate) + '.vp9'),
                           logFile=os.path.join(logDir, 'log_' + video['fname']+'_vp9_' + str(rate)))
        toc = time.time()
        times.write(str(toc - tic) + '\n'), times.flush()

times.close()


# 2. Collect stats

for video in videos:
    trueBitrates = np.zeros((3, 9))
    psnrs = np.zeros((3,9))

    for idx_codec, codec in enumerate(('h264', 'h265', 'vp9')):
        for idx_rate, rate in enumerate(bitrates):
            psnr, trueBitrate = encode.get_stats(video, logDir, codec, rate)

            trueBitrates[idx_codec, idx_rate] = trueBitrate
            psnrs[idx_codec, idx_rate] = psnr

    import matplotlib.pyplot as  plt
    colors = ('k--', 'g-^', 'r-s')

    plt.figure()
    for codec in range(3):
        plt.plot(trueBitrates[codec], psnrs[codec], colors[codec], linewidth=2.5)

    plt.title(video['show'])
    plt.rcParams.update({'font.size': 22})
    plt.gcf().subplots_adjust(bottom=0.15)
    plt.grid(b=True, which='both', color='0.65', linestyle='-')
    plt.legend(('H264', 'H265', 'VP9'), loc=0)
    plt.xlabel('bitrate [kbps]')
    plt.ylabel('PSNR [db]')
    plt.savefig('psnr_'+video['show']+'.png')


# 3. Collect encoding times

enc = np.zeros((3,11,9))

with open('./out/encoding_times.txt') as f:
    contents = f.read().splitlines()

for rate_idx, _  in enumerate(bitrates):
    for file_idx in range(11):
        for codec_idx in range(3):
            enc[codec_idx, file_idx, rate_idx] = contents[rate_idx*11*4 + file_idx * 4 + codec_idx + 1]

mean_enc = np.mean(np.mean(enc, axis=2), axis=1)
std_enc = np.std(np.mean(enc, axis=2), axis=1)

print(mean_enc)
print(std_enc)

