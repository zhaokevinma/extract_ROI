import nibabel as nib

# Read file 
file = 'example.nii'
img = nib.load(file)    

# Read and print headers
print(img.header)
