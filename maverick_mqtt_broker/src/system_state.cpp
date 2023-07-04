#include "system_state.h"

system_state::system_state(){
    state_map.clear();
}
bool system_state::update_state(std::string state_var, void* item){
    //make a copy of the item to prevent loss by mem free ops and assign to key
    if (state_var.find("int_") != std::string::npos){
        state_map[state_var] = item;
    }else if (state_var.find("bool_") != std::string::npos){
        state_map[state_var] = item;
    } else if(state_var.find("str_") != std::string::npos){
        int len = strlen((char*)item);
        char* x = (char*) malloc(len+1);
        strncpy(x, (char*) item,len+1);
        if (state_map.find(state_var)!= state_map.end()){
            void * a = state_map[state_var];
            free(a);
        }
        state_map[state_var] = (void*) x;
    } else{
        return false;
    }
    return true;
    
}
void* system_state::retrieve_state(std::string state_var){
    if (state_map.find(state_var) == state_map.end()){
        return NULL;
    }else{
        return state_map[state_var];
    }
}
system_state::~system_state(){
    state_map.clear();
}
