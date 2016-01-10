import sys, os, glob

if len(sys.argv) != 2:
    print '  Specify a directory with frames'
    sys.exit()

input_dir = sys.argv[1]
if not os.path.isdir(input_dir):
    print '  No such directory'
    sys.exit()

frame_format = raw_input('Frame format: (png) ')
if not frame_format:
    frame_format = 'png'

slide_duration = raw_input('Slide duration in seconds: (1) ')
if not slide_duration:
    slide_duration = 1
else:
    slide_duration = int(slide_duration)

multiple = raw_input('Repeat movie horizontally how many times? (1) ')
if not multiple or int(multiple) < 1:
    multiple = 1
else:
    multiple = int(multiple)

output_movie_format = raw_input('Output movie format: (mp4) ')
if not output_movie_format:
    output_movie_format = 'mp4'

output_movie_name = raw_input('Output movie name: (movie) ')
if not output_movie_name:
    output_movie_name = 'movie'

# Get the list of frames
frames = [os.path.basename(s.replace(' ', '\ ')) for s in glob.glob(os.path.join(input_dir, '*.' + frame_format))]

if not frames:
    print '  No frames found. Does your directory contain {} files?'.format(frame_format)
    sys.exit()
else:
    s = 's' if len(frames) > 1 else ''
    print '  {} frame{} found'.format(len(frames), s)

# Create a temporary directory to hold merged frames
if not os.path.exists('./merged_frames'):
    os.makedirs('./merged_frames')

# Merge frames
print '  Merging frames...'
for f in frames:
    command = 'convert +append {0} {1}'.format(' '.join([os.path.join(input_dir, f)] * multiple), os.path.join('./merged_frames', f))
    os.system(command)

# Make movie from frames
print '  Creating video from frames...'
command = "ffmpeg -framerate 1/{} -pattern_type glob -i '{}/*.{}' -c:v libx264 -pix_fmt yuv420p {}".format(slide_duration, './merged_frames', frame_format, './' + output_movie_name + '.' + output_movie_format)
print command
os.system(command)