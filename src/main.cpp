#include <iomanip>
#include <iostream>
#include <string>
#include <sstream>
#include <algorithm>
#include <iterator>
#include <stdio.h>
#include <vector>
#include <iterator>

using namespace std;
const int MAX_BUFFER = 255;


void parse_python_result(const string result){
   istringstream iss(result);
   vector<string> words{istream_iterator<string>{iss},
                      istream_iterator<string>{}};
   if (words[0]!="INSERT_OK"){
      cout << "Ops, something went wrong while inserting new object" << endl;
   }else{
      cout << "New object correctly added to the scenario" << endl;
   }
   if(words.size() != 5){
      cout << "Cannot retrieve state for the specified object id";
   }else{
      cout << "RETRIEVED STATE:" << endl;
      string position_x = words[1];
      string position_y = words[2];
      string rotation = words[3];
      string velocity = words[4];
      cout << "\tPosition: " << position_x << "," << position_y << endl;
      cout << "\tRotation: " << rotation << endl;
      cout << "\tVelocity: " << velocity << endl;
   }
}


string call_python_script(int new_id,float pos_x,float pos_y,float rotation, float velocity, int get_state_id){
   string stdout;
   char buffer[MAX_BUFFER];
   ostringstream cmd;
   cmd << "python simple_reader.py " << new_id << " " << pos_x << " " << pos_y << " " << rotation << " " << velocity << " --get-state " << get_state_id;
   string cmd_str = cmd.str();
   FILE *stream = popen(cmd_str.c_str(), "r");
   while ( fgets(buffer, MAX_BUFFER, stream) != NULL )
   stdout.append(buffer);
   pclose(stream);
   return stdout;
}
void add_and_verify(){
   cout << "Running dumb test: insert something, query the very same object and match outout:" << endl;
   int new_id = 123;
   float pos_x = 12.5;
   float pos_y = 14.5;
   float rotation = 0.1;
   float velocity = 3.4;
   string result = call_python_script(new_id,pos_x,pos_y,rotation,velocity,new_id);
   string expected_return = "INSERT_OK 12.5 14.5 0.1 3.4\n";
   if (result == expected_return){
      cout << "====TEST PASSED" << endl;
   }else{
      cout << "====Ops, looks like input data for the new object does not match the queried one" << endl;
   }
}
void insert_another_and_query(){
   int new_id = 123;
   float pos_x = 12.5;
   float pos_y = 14.5;
   float rotation = 0.1;
   float velocity = 3.4;
   int query_id = 11434;
   string result = call_python_script(new_id,pos_x,pos_y,rotation,velocity,query_id);
   parse_python_result(result);
}
int main() {
   add_and_verify();
   insert_another_and_query();
   exit(0);
}