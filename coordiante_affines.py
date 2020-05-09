import nibabel as nib
import matplotlib.pyplot as plt

def show_slices(slices):
    fig, axes = plt.subplots(1, len(slices))
    for i, slice in enumerate(slices):
        axes[i].imshow(slice.T, cmap = "gray", origin = "lower")


epi_img = nib.load('someones_epi.nii.gz')
epi_img_data = epi_img.get_fdata()
print("Data Shape: ", epi_img_data.shape)


slice_0 = epi_img_data[26, :, :]
slice_1 = epi_img_data[:, 30, :]
slice_2 = epi_img_data[:, :, 16]
show_slices([slice_0, slice_1, slice_2])
plt.suptitle("Center slices for EPI image")

plt.savefig('test.jpg')