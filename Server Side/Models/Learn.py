import os

def learn_from_dataset(dataset_path, training_amount):
    os.system(f'cmd /c "convert_dir_to_note_sequences \ --input_dir={dataset_path} \ --output_file={dataset_path}/tmp/notesequences.tfrecord \ --recursive"')
    os.system(f'cmd /c "polyphony_rnn_create_dataset \ --input={dataset_path}/tmp/notesequences.tfrecord \ --output_dir={dataset_path}/tmp/polyphony_rnn/sequence_examples \ --eval_ratio=0.10"')
    os.system(f'cmd /c "polyphony_rnn_train \ --run_dir={dataset_path}/tmp/polyphony_rnn/logdir/run1 \ --sequence_example_file={dataset_path}/tmp/polyphony_rnn/sequence_examples/training_poly_tracks.tfrecord \ --hparams="batch_size=64,rnn_layer_sizes=[128,128,128]" \ --num_training_steps={training_amount}"')


def generate_output(dataset_path, outputs_amount):
    os.system(f'cmd /c "polyphony_rnn_generate \ --run_dir={dataset_path}/tmp/polyphony_rnn/logdir/run1 \ --hparams="batch_size=64,rnn_layer_sizes=[128,128,128]" \ --output_dir={dataset_path}/tmp/polyphony_rnn/generated \ --num_outputs={outputs_amount} \ --num_steps=128 \ --primer_pitches="[67,64,60]" \ --condition_on_primer=true \ --inject_primer_during_generation=false"')