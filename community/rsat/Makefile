override CFLAGS += -std=c11 -Wall -Wextra -I/usr/include/z3/ `pkg-config --cflags libbsd-overlay` -fopenmp
override LDFLAGS  += -std=c11 -lm -lz3 `pkg-config --libs libbsd-overlay` -fopenmp

EXEC = rsat

CSRCS      = $(wildcard *.c */*.c)
CHDRS      = $(wildcard *.h */*.h)

NAMEOBJDIR = objs
OBJDIR = $(shell mkdir -p $(NAMEOBJDIR); echo $(NAMEOBJDIR))
NOM = $(basename $(notdir $(CSRCS)))
COBJS = $(addprefix $(OBJDIR)/, $(addsuffix .o, $(NOM)))

DCOBJS = $(addsuffix d, $(COBJS))

.PHONY: debug

all: $(EXEC)
debug: $(EXEC)_d

#  -fsanitize=address -fno-omit-frame-pointer -static-libasan

$(OBJDIR)/%.od: CFLAGS += -g -Wfatal-errors -fsanitize=address -fno-omit-frame-pointer -static-libasan
$(OBJDIR)/%.o: CFLAGS += -O3

$(EXEC)_d: LDFLAGS += -g -Wfatal-errors -fsanitize=address -fno-omit-frame-pointer -static-libasan
$(EXEC): LDFLAGS += -O3

$(EXEC): $(COBJS)
$(EXEC)_d: $(DCOBJS)

$(OBJDIR)/%.o $(OBJDIR)/%.od: */%.c
	$(CC) $(CFLAGS) -c $< -o $@

$(EXEC) $(EXEC)_d:
	$(CC) $^ -o $@ $(LDFLAGS)

clean:
	rm -f $(EXEC) "$(EXEC)_d" "$(EXEC).sif"
	rm -rf objs

singularity:
	rm -f "$(EXEC).sif"
	singularity build --fakeroot "$(EXEC).sif" "$(EXEC).def"

