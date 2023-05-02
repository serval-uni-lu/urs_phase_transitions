CXXFLAGS += -std=c++14 -Wall -Wextra -fopenmp -pthread
LDFLAGS  += -std=c++14 -fopenmp -pthread

ifeq ($(STATS),1)
CXXFLAGS += -DSTATS
endif

EXEC = cnf_to_lp

CSRCS      = $(wildcard *.cpp */*.cpp)
CHDRS      = $(wildcard *.hpp */*.hpp)

NAMEOBJDIR = objs
OBJDIR = $(shell mkdir -p $(NAMEOBJDIR); echo $(NAMEOBJDIR))
NOM = $(basename $(notdir $(CSRCS)))
COBJS = $(addprefix $(OBJDIR)/, $(addsuffix .o, $(NOM)))

DCOBJS = $(addsuffix d, $(COBJS))

.PHONY: debug

all: $(EXEC)
debug: $(EXEC)_d

# ASAN:  -fsanitize=address -fno-omit-frame-pointer -static-libasan
$(OBJDIR)/%.od: CXXFLAGS += -g -Wfatal-errors
$(OBJDIR)/%.o: CXXFLAGS += -O3

$(EXEC)_d: LDFLAGS += -g -Wfatal-errors
$(EXEC): LDFLAGS += -O3

$(EXEC): $(COBJS)
$(EXEC)_d: $(DCOBJS)

$(OBJDIR)/%.o $(OBJDIR)/%.od: */%.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

$(EXEC) $(EXEC)_d:
	$(CXX) $^ -o $@ $(LDFLAGS)

clean:
	rm -f $(EXEC) "$(EXEC)_d" "$(EXEC).sif"
	rm -rf objs

singularity:
	rm -f "$(EXEC).sif"
	singularity build --fakeroot "$(EXEC).sif" "$(EXEC).def"

