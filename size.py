import scipy.io as sio

contents = sio.loadmat("/Users/suhyunkim/git/Pasion/diving.mat")
print(len(contents))
tracked = contents['boxes_tracked_wholevideo']
print(tracked)

# 298387
print(len(tracked))
# (298387, 107)
print(tracked.shape)

# (107,)
print(tracked[0].shape)
tracked[0] = tracked[0][:104]
print(new.shape)
# print(f'this: {tracked[291855]}')

