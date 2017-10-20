from models import mnist_mlp_benchmark
import upload_benchmarks_bq as bq
import argparse
import tensorflow as tf
import theano
import cntk
import keras

parser = argparse.ArgumentParser()
parser.add_argument('--keras_backend', default="tensorflow",
                    help='Keras backend being used to run benchmarks.')

args = parser.parse_args()
print(args.keras_backend)


def get_keras_backend_version(backend_type):
  if str(backend_type) == "tensorflow":
    return tf.__version__
  if str(backend_type) == "theano":
    return theano.__version__
  if str(backend_type) == "cntk":
    return cntk.__version__
  return "undefined"

model = mnist_mlp_benchmark.MnistMlpBenchmark()
model.benchmarkMnistMlp()

bq.upload_metrics_to_bq(model.get_testname(), model.get_totaltime(),
                     model.get_iters(), model.get_batch_size(),
                     args.keras_backend, get_keras_backend_version(args.keras_backend),
                     "1", "3.75", "GB",
                     "GCP", "n1-standard-1", keras.__version__,model.get_sampletype())
