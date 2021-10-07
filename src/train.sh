
#!/bin/bash

CATEGORIES=(
			#bottle
			# grid
			#leather
			#metal_nut
			#pill
			#screw
			#tile
			#toothbrush
			 transistor
            #wood
			 #   zipper
			)

for DataType in "${CATEGORIES[@]}"
do 
    echo "resnet18_training $DataType" 
    python3 resnet18_training.py --dataset $DataType
    echo "Done"

    echo "teacher_training.py $DataType"
    python3 teacher_training.py --dataset $DataType --patch_size 33
    echo "Done"

    echo "students_training.py $DataType"
    python students_training.py --dataset $DataType --patch_size 33 --n_students 3
    echo "Done"
done

# echo "resnet18_training"
# python3 resnet18_training.py --dataset $DataType
# echo "Done"

# echo "teacher_training.py"
# python3 teacher_training.py --dataset $DataType --patch_size 33
# echo "Done"

# echo "students_training.py"
# python students_training.py --dataset bottle  --patch_size 33 --n_students 3
# echo "Done"

# echo "anomaly_detection.py"
# python anomaly_detection.py --dataset carpet --patch_size 33 
# echo "Done"
