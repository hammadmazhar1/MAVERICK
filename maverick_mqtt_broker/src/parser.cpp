# include "parser.h"




void remove_space(char *formula)
{
	int i, j, len =strlen(formula);
	//char msg[50];
	
	for(i=0,j=0; j<len;++j)
	{
		//snprintf(msg, sizeof(msg),"i:%d ,j:%d, len:%d",i,j,len);
		//error_message_without_return(msg);
		if(formula[j]==' ')continue;
		formula[i]=formula[j]; 
		++i;
	}
	formula[i]='\0';
}

int next_token(char *rFormula, char *token, int cIndex, int len)
{
	int j = cIndex, i=0; 
    // std::cout << rFormula<<std::endl;
	for(;j<len;++j)
	{
		if(rFormula[j]=='(' || rFormula[j]==')' || rFormula[j] == ',')
		{
            // std::cout<<i<<std::endl;
			assert(i>0);
			token[i]='\0';
			return i;
		}
		token[i]=rFormula[j]; ++i; 
	}
	token[i]='\0';
	return i;

}
int error_message(const char * msg)
{
	printf("ERROR:%s\n",msg);
	return 1 ; 
}

void error_message_without_return(const char * msg)
{
	printf("ERROR:%s\n",msg);
}



pltl_parser::pltl_parser()
{
    globalIndex = 0 ; 
}
int pltl_parser::getGlobalIndex()
{
    return globalIndex ; 
}



std::pair< int , ast_node *> pltl_parser::handle_binop(char * formula, int cIndex, int len, ast_node * current_node, nodeType n)
{
        current_node->nType = n ; 
        ast_node *c1 = new ast_node();
        ast_node *c2 = new ast_node();

        assert(cIndex < len); assert(formula[cIndex] =='('); ++cIndex;

        std::pair<int, ast_node*> r1 = parse_formula(formula, cIndex, len, c1);
        current_node->add_children(r1.second); cIndex = r1.first ;
        // std::cout<<formula<<std::endl;
        assert(cIndex < len); assert(formula[cIndex] ==','); ++cIndex;

        std::pair<int, ast_node*> r2 = parse_formula(formula, cIndex, len, c2);
        current_node->add_children(r2.second); cIndex = r2.first ;
        // std::cout<< "cIndex:" << cIndex <<", " << "len:" << len << std::endl;
        assert(cIndex < len); assert(formula[cIndex] ==')'); ++cIndex;

        return std::make_pair(cIndex, current_node);
    
}

std::pair< int , ast_node *> pltl_parser::handle_unop(char * formula, int cIndex, int len, ast_node * current_node, nodeType n)
{
        current_node->nType = n ; 
        ast_node *c1 = new ast_node();

        assert(cIndex < len); assert(formula[cIndex] =='('); ++cIndex;

        std::pair<int, ast_node*> r1 = parse_formula(formula, cIndex, len, c1);
        current_node->add_children(r1.second); cIndex = r1.first ;
    
        // std::cout<< "cIndex:" << cIndex <<", " << "len:" << len << std::endl;
        assert(cIndex < len); assert(formula[cIndex] ==')'); ++cIndex;

        return std::make_pair(cIndex, current_node);

}


std::pair< int , ast_node *> pltl_parser::parse_formula( char * formula, int cIndex, int len, ast_node * current_node)
{
    if(cIndex >= len)
    {
        error_message_without_return("currentIndex greater than length");		
        return std::make_pair(cIndex, (ast_node*) NULL); 
    }
    char tok[1024] ; 
    int l = next_token(formula, tok, cIndex, len);
    
    cIndex += l ; 
    current_node->aIndex = globalIndex; ++globalIndex; 
    // #ifdef WITH_POLICY_CHECK 
    //     printf("DEBUG TOKEN: %s\n",tok);
    // #endif 
    if(strcmp(tok,"=>")==0)     return handle_binop(formula, cIndex, len, current_node, LIMPLY); 
    else if(strcmp(tok,"&")==0) return handle_binop(formula, cIndex, len, current_node, LAND);
    else if(strcmp(tok,"|")==0) return handle_binop(formula, cIndex, len, current_node, LOR);
    else if(strcmp(tok,"S")==0) return handle_binop(formula, cIndex, len, current_node, since);


    else if(strcmp(tok,"!")==0) return handle_unop(formula, cIndex, len, current_node, LNOT) ; 
    else if(strcmp(tok,"Y")==0) return handle_unop(formula, cIndex, len, current_node, yesterday) ;
    else if(strcmp(tok,"H")==0) return handle_unop(formula, cIndex, len, current_node, historically) ;
    else if(strcmp(tok,"O")==0) return handle_unop(formula, cIndex, len, current_node, once) ;


    else 	if(strcmp(tok,"TRUE")==0)
    {
        current_node->nType = LTRUE ;
        current_node->nValue=NULL; 
        return std::make_pair(cIndex, current_node) ; 

    }
    else 	if(strcmp(tok,"FALSE")==0)
    {
        current_node->nType = LFALSE ;
        current_node->nValue=NULL; 
        return std::make_pair(cIndex, current_node) ; 
    }
    else
    {
        current_node->nType = prop ; 
        current_node->nValue = (char*) malloc(sizeof(char)* (l+1)); 
        strcpy(current_node->nValue, tok);
        return std::make_pair(cIndex, current_node) ; 
    }
}



ast_node * pltl_parser::parse_formula_to_ast(char *formula, ast_node * current_node)
{
    remove_space(formula); 

    std::pair< int , ast_node *> ret = parse_formula(formula, 0, strlen(formula), current_node) ; 
    current_node = ret.second ; 		
    return current_node ;
}
