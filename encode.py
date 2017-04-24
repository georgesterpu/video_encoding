import os
import subprocess as sp

def encode_h264(video, bitrate, outputFile, logFile):

    log = open(logFile, 'w')

    pass1 = ['ffmpeg', '-y',
            '-s', video['width']+'x'+video['height'],
            '-f', 'rawvideo',
            '-r', video['framerate'],
            '-i', os.path.join(video['fpath'], video['fname']),
            '-vcodec', 'libx264',
            '-t', '10',
            '-preset', 'veryslow',
            '-tune', 'psnr',
            '-profile', 'high',
            '-pass', '1',
            '-b:v', bitrate+'k',
outputFile]

    print(sp.list2cmdline(pass1))
    pipe1 = sp.Popen(pass1, stdout=log, stderr=log)
    pipe1.wait()

    pass2 = ['ffmpeg','-y',
             '-s', video['width'] + 'x' + video['height'],
             '-f', 'rawvideo',
             '-r', video['framerate'],
             '-i', os.path.join(video['fpath'], video['fname']),
             '-vcodec', 'libx264',
             '-t', '10',
             '-preset', 'veryslow',
             '-tune', 'psnr',
             '-psnr',
             '-profile', 'high',
             '-pass', '2',
             '-b:v', bitrate+'k',
             outputFile]

    print(sp.list2cmdline(pass2))
    pipe2 = sp.Popen(pass2, stdout=log, stderr=log)
    pipe2.wait()

    log.close()


def encode_h265(video, bitrate, outputFile, logFile):

    log = open(logFile, 'w')
    pass1 = ['x265',
           '--csv', logFile + '.csv',
           '--input-res', video['width'] + 'x' + video['height'],
           '--fps', video['framerate'],
           '--tune', 'psnr',
           '--psnr',
           '--preset', 'veryslow',
           '--keyint', '-1',
           '--bitrate', bitrate,
           '--pass', '1',
           '--tu-intra-depth', '2',
           '--tu-inter-depth', '2',
           # '--recon', os.path.join(os.path.split(outputFile)[0], video['fname']+'_recon.yuv'), # is this useful now ?
           '--input', os.path.join(video['fpath'], video['fname']),
           '-o', outputFile]

    print(sp.list2cmdline(pass1))
    pipe = sp.Popen(pass1, stdout=log, stderr=log)
    pipe.wait()

    pass2 = ['x265',
           '--csv', logFile + '.csv',
           '--input-res', video['width'] + 'x' + video['height'],
           '--fps', video['framerate'],
           '--tune', 'psnr',
           '--psnr',
           '--preset', 'veryslow',
           '--keyint', '-1',
           '--bitrate', bitrate,
           '--pass', '2',
           '--tu-intra-depth', '2',
           '--tu-inter-depth', '2',
           # '--recon', os.path.join(os.path.split(outputFile)[0], video['fname']+'_recon.yuv'), # is this useful now ?
           '--input', os.path.join(video['fpath'], video['fname']),
           '-o', outputFile]

    print(sp.list2cmdline(pass2))
    pipe = sp.Popen(pass2, stdout=log, stderr=log)
    pipe.wait()

    log.close()


def encode_vp9(video, bitrate, outputFile, logFile):
    log = open(logFile, 'wb')
    cmd = ['vpxenc',
           '--width='+video['width'],
           '--height='+video['height'],
           '--i420',
           '--fps='+video['framerate'],
           '-o', outputFile,
           os.path.join(video['fpath'], video['fname']),
           '--good', # Use Good Quality Deadline
           '--cpu-used=0', # impacts quality, 0 for best
           '-t', '3', # number of threads
           '--end-usage=0', # rate control mode in [0:vbr, cbr,cq,q]
           '-p', '2', # two passes
           '--limit=300', #Stop encoding after n input frames
           '--codec=vp9',
           '--kf-max-dist=9999', # Maximum keyframe interval (frames)
           '--psnr',
           '--target-bitrate='+bitrate]

    print(sp.list2cmdline(cmd))
    pipe = sp.Popen(cmd, stdout=log, stderr=log)
    pipe.wait()

    log.close()


def get_stats(video, logdir, codec, bitrate):

    logFile = os.path.join(logdir, 'log_' + video['fname'] + '_' + codec + '_' + str(bitrate))

    if codec == 'h264':
        psnr, trueBitrate = get_stats_h264(logFile)
    elif codec == 'h265':
        psnr, trueBitrate = get_stats_h265(logFile)
    elif codec == 'vp9':
        psnr, trueBitrate = get_stats_vp9(logFile)

    else:
        raise Exception('Unknown codec')

    return psnr, trueBitrate


def get_stats_h264(logFile):
    with open(logFile, 'r') as log:
        line = log.read().splitlines()[-1]
        ii = line.find('Y:')
        PSNR_Y = float(line[ii+2:ii+8])

        br = line.split(' ')[-1]
        br = br.split(':')[1]
        trueBitrate = float(br)

    return PSNR_Y, trueBitrate



def get_stats_h265(logFile):

    with open(logFile+'.csv', 'r') as f:
        contents = f.read().splitlines()[-1] # last line is the last pass
        elems = contents.split(',')
        PSNR_Y = float(elems[5])
        trueBitrate = float(elems[4])

    return PSNR_Y, trueBitrate


def get_stats_vp9(logFile):
    import re
    with open(logFile, 'r') as log:
        contents = log.read().splitlines()[-2:]
        br = contents[0]
        br = re.sub( '\s+', ' ', br ).strip()
        br = br.split(' ')[6]
        trueBitrate = float(br.split('b/s')[0]) / 1024

        PSNR_Y = float(contents[1].split(' ')[6])

    return PSNR_Y, trueBitrate
