package edu.gatech.cse6242;

import org.apache.hadoop.fs.Path;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapreduce.*;
import org.apache.hadoop.util.*;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

import java.io.IOException;


public class Q1 {

  public static class GraphMapper extends Mapper<LongWritable, Text, IntWritable, IntWritable> {
    @Override
    public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
      // Tokenize it by tab
      String dataStr = value.toString();
      String[] data = dataStr.split("\t");
      //System.out.println("******"+dataStr);
  
      // get the target and weight
      IntWritable target = new IntWritable(Integer.parseInt(data[1]));
      IntWritable weight = new IntWritable(Integer.parseInt(data[2]));
      //System.out.println(target + " "+weight);
  
      // write into the output
      // make them in tuple (target, weight)
      context.write(target, weight);
    }
  }
  
  public static class GraphReducer extends Reducer<IntWritable, IntWritable, IntWritable, IntWritable> {
    @Override
    public void reduce(IntWritable key, Iterable<IntWritable> values, Context context)
        throws IOException, InterruptedException {
      
      int total = 0;
      for (IntWritable value : values)
        total += value.get();
  
      // write into the output
      context.write(key, new IntWritable(total));
    }
  }
  

  public static void main(String[] args) throws Exception {
    Configuration conf = new Configuration();
    Job job = Job.getInstance(conf, "Q1");

    /* TODO: Needs to be implemented */
    // This is the main class for our fat jar file
    job.setJarByClass(Q1.class);

	  //Set our map and reduce class to our project
    job.setMapperClass(GraphMapper.class);
    job.setReducerClass(GraphReducer.class);

    //output is key value of both int type.
    job.setOutputKeyClass(IntWritable.class);
    job.setOutputValueClass(IntWritable.class);

    FileInputFormat.addInputPath(job, new Path(args[0]));
    FileOutputFormat.setOutputPath(job, new Path(args[1]));
    System.exit(job.waitForCompletion(true) ? 0 : 1);
  }
}
