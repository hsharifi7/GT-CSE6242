package edu.gatech.cse6242;

import org.apache.hadoop.fs.Path;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapreduce.*;
import org.apache.hadoop.util.*;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import java.io.IOException;

public class Q4 {

  public static void main(String[] args) throws Exception {
    Configuration conf1 = new Configuration();

    String outputPath = args[1];

    Job stepOne = Job.getInstance(conf1, "Q4-1");

    // This is the main class for our fat jar file
    stepOne.setJarByClass(Q4.class);

    // This is the first step in creating (key, value) pairs
    stepOne.setMapperClass(StepOneMapper.class);
    stepOne.setReducerClass(StepOneReducer.class);

    // define the type of the (key, value) 
    stepOne.setOutputKeyClass(IntWritable.class);
    stepOne.setOutputValueClass(IntWritable.class);

    // let's write it in the azure. The output of this step is the input 
    // for the next step
    FileInputFormat.addInputPath(stepOne, new Path(args[0]));
    FileOutputFormat.setOutputPath(stepOne, new Path(outputPath+"firstStep"));

    stepOne.waitForCompletion(true);

    /**********************Second Step ********************/

    Configuration conf2 = new Configuration();

    Job stepTwo = Job.getInstance(conf2, "Q4-2");

    // Running the same fat jar
    stepTwo.setJarByClass(Q4.class);

    // This is the second step in creating (key, value) pairs
    stepTwo.setMapperClass(StepTwoMapper.class);
    stepTwo.setReducerClass(StepTwoReducer.class);

    // define the type of the (key, value)
    stepTwo.setOutputKeyClass(IntWritable.class);
    stepTwo.setOutputValueClass(IntWritable.class);

    // let's write the final result in the azure blob container
    // The input is from the previous step
    FileInputFormat.addInputPath(stepTwo, new Path(outputPath+"firstStep"));
    FileOutputFormat.setOutputPath(stepTwo, new Path(outputPath));

    System.exit(stepTwo.waitForCompletion(true) ? 0 : 1);
  }

  static class StepOneMapper extends Mapper<LongWritable, Text, IntWritable, IntWritable> {
    @Override
    public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
      // split each line of data
      String dataStr = value.toString();
      if (dataStr.length() > 1) {
        String[] data = dataStr.split("\t");

        // get the source and target from each line in the file
        IntWritable source = new IntWritable(Integer.parseInt(data[0]));
        IntWritable target = new IntWritable(Integer.parseInt(data[1]));

        // pair every source with 1 and every target with -1
        // (source, 1) , (target, -1)
        IntWritable posOne = new IntWritable(1);
        IntWritable negOne = new IntWritable(-1);

        // create the pairs
        context.write(source, posOne);
        context.write(target, negOne);
      }
    }
  }

  static class StepOneReducer extends Reducer<IntWritable, IntWritable, IntWritable, IntWritable> {
    @Override
    public void reduce(IntWritable key, Iterable<IntWritable> values, Context context)
        throws IOException, InterruptedException {
      
      // calculate the sum with the same key
      // those targets are -1 which makes them to get substracted
      // difference = out-degree - in-degree
      int sum = 0;
      for (IntWritable value : values)
        sum += value.get();

      // write key value blob azure output
      context.write(key, new IntWritable(sum));
    }
  }

  static class StepTwoMapper extends Mapper<LongWritable, Text, IntWritable, IntWritable> {
    @Override
    public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
      // split each line of data
      String dataStr = value.toString();
      if (dataStr.length() > 1) {
        String[] data = dataStr.split("\t");

        // get the diff and make it the key to the next key value pair
        // (difference, 1) and reducre on these pairs
        IntWritable diffrance = new IntWritable(Integer.parseInt(data[1]));
        IntWritable valueOne = new IntWritable(1);

        // write key value hadoop output
        context.write(diffrance, valueOne);
      }
    }
  }

  static class StepTwoReducer extends Reducer<IntWritable, IntWritable, IntWritable, IntWritable> {
    @Override
    public void reduce(IntWritable key, Iterable<IntWritable> values, Context context)
        throws IOException, InterruptedException {

      // calculate the total sum here
      // this is like the reducer in step one
      int sum = 0;
      for (IntWritable value : values)
        sum += value.get();

      // write key value blob azure output
      context.write(key, new IntWritable(sum));
    }
  }
}
