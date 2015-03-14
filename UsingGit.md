# Using Git with Pinax #

If you choose to use git, who wouldn't, read this to learn how to setup Pinax. Unfortunately checking out the Pinax source code is not as simple as a ` git svn clone `. Pinax contains some svn:externals that just do not work with only a ` git-svn clone `. Go and grab git-svn-clone-externals from http://github.com/andrep/git-svn-clone-externals/tree/master and place it on your `PATH` and `chmod +x` it. Once you have done that it is as simple as doing:

```
git svn clone http://svn.pinaxproject.com/pinax/trunk pinax
cd pinax/apps/external_apps
git-svn-clone-externals
```

You are all set. `git-svn-clone-externals` is very basic in nature. It simply:

  * git svn clone each external into a .git\_externals/ directory.
  * symlink the cloned repository in .git\_externals/ to the proper directory name.
  * add the symlink and .git\_externals/ to the .git/info/excludes/ file, so that you're not pestered about it when performing a git status.