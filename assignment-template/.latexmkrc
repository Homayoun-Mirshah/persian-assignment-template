$pdf_mode = 5;
$out_dir = 'build';
$xelatex = 'xelatex -shell-escape -synctex=1 -interaction=nonstopmode -file-line-error -halt-on-error %O %S';

# Keep TeXstudio and terminal builds on the same environment, without changing
# the user's global PATH or installing anything during ordinary compilation.
use Cwd qw(abs_path);
use File::Spec;
use File::Glob qw(bsd_glob);
my $assignment_root = abs_path('.');
my $assignment_sep = ($^O eq 'MSWin32') ? ';' : ':';
my $assignment_bin = File::Spec->catdir($assignment_root, 'tools', 'bin');
if (-f File::Spec->catfile($assignment_bin, 'latexminted.cmd')) {
    $ENV{'PATH'} = $assignment_bin . $assignment_sep . $ENV{'PATH'};
} elsif ($^O eq 'MSWin32' && $ENV{'LOCALAPPDATA'}) {
    # Python's Windows install manager and the older per-user installer.
    # Prefer the real Python entry point over TeX Live's optional wrapper.
    my @assignment_appdata = ($ENV{'LOCALAPPDATA'});
    push @assignment_appdata, $ENV{'USERPROFILE'} . '/AppData/Local'
        if $ENV{'USERPROFILE'};
    my @assignment_python_bins;
    for my $assignment_appdata (@assignment_appdata) {
        push @assignment_python_bins,
            bsd_glob($assignment_appdata . '/Python/pythoncore-*/Scripts'),
            bsd_glob($assignment_appdata . '/Programs/Python/Python*/Scripts');
    }
    for my $assignment_scripts (reverse sort @assignment_python_bins) {
        if (-f File::Spec->catfile($assignment_scripts, 'latexminted.exe')) {
            $ENV{'PATH'} = $assignment_scripts . ';' . $ENV{'PATH'};
            last;
        }
    }
}
my $assignment_tex = File::Spec->catdir($assignment_root, 'texmf', 'tex', 'latex');
if (-d $assignment_tex) {
    $assignment_tex =~ s!\\!/!g;
    $ENV{'TEXINPUTS'} = $assignment_tex . '//' . $assignment_sep
        . ($ENV{'TEXINPUTS'} // '') . $assignment_sep;
}
