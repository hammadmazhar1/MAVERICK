#ifndef __CONSTATE_H__
#define __CONSTATE_H__

# include "headers.h"

typedef std::set< std::string > snapshot;

class sys_state{
	public:
	snapshot s;

	bool isTrue(std::string prop){
		std::set<std::string>::iterator it = s.find(prop) ;
		return (it!= s.end()); 
	}
	
	~sys_state(){
		s.clear();
	}
};

#endif 